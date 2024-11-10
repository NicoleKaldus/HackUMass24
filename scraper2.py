import json
import praw
import pandas as pd
import re
import pprint
import time
from prawcore.exceptions import TooManyRequests, ResponseException

class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.base_delay = 1  # Start with 1 second delay
        self.max_retries = 3
        self.current_delay = self.base_delay

    def with_rate_limit(self, func, *args, **kwargs):
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except TooManyRequests:
                if attempt == self.max_retries - 1:
                    raise

                print(f"Rate limited, waiting {self.current_delay} seconds...")
                time.sleep(self.current_delay)
                self.current_delay *= 2  # Exponential backoff
            except ResponseException as e:
                print(f"Reddit API error: {e}")
                time.sleep(self.current_delay)
                self.current_delay *= 2

        self.current_delay = self.base_delay  # Reset delay after successful request
        return None

    @staticmethod
    def clean_text(text):
        return re.sub(r"[^a-zA-Z0-9\s/?:\n.']", '', text)

    def process_more_comments(self, more_comments):
        comments = []
        try:
            # Load more comments with rate limiting
            loaded_comments = self.with_rate_limit(more_comments.comments)
            if loaded_comments:
                for comment in loaded_comments:
                    comment_tree = self.comment_tree(comment)
                    if comment_tree:
                        comments.append(comment_tree)
        except Exception as e:
            print(f"Error loading more comments: {e}")
        return comments

    def comment_tree(self, comment):
        # Handle MoreComments object
        if isinstance(comment, praw.models.MoreComments):
            return self.process_more_comments(comment)

        def _get_comment_data():
            tree = {
                "user": "",
                "text": "",
                "replies": []
            }

            try:
                if hasattr(comment, 'body') and len(comment.body) > 20:
                    tree["text"] = comment.body
                if hasattr(comment, 'author') and comment.author:
                    tree["user"] = comment.author.name
                else:
                    tree["user"] = "[deleted]"
            except Exception as e:
                print(f"Error processing comment: {e}")

            return tree

        tree = self.with_rate_limit(_get_comment_data)
        if tree is None:
            return {"user": "", "text": "", "replies": []}

        # Process replies with rate limiting
        if hasattr(comment, 'replies'):
            for reply in comment.replies:
                reply_tree = self.comment_tree(reply)
                if isinstance(reply_tree, list):  # Handle case where reply_tree is from MoreComments
                    tree["replies"].extend(reply_tree)
                elif reply_tree:
                    tree["replies"].append(reply_tree)

        return tree

    def create_submission_tree(self, submission):
        def _get_submission_data():
            tree = {
                "user": "",
                "title": submission.title,
                "text": "",
                "replies": []
            }

            try:
                tree["user"] = submission.author.name if submission.author else "[deleted]"
            except:
                print("Author name error")
                tree["user"] = "[deleted]"

            if len(submission.selftext) > 20:
                tree["text"] = submission.selftext

            return tree

        tree = self.with_rate_limit(_get_submission_data)
        if tree is None:
            return None

        submission.comment_sort = "hot"

        # Handle comments and MoreComments objects
        if hasattr(submission, 'comments'):
            for comment in submission.comments:
                comment_tree = self.comment_tree(comment)
                if isinstance(comment_tree, list):  # Handle case where comment_tree is from MoreComments
                    tree["replies"].extend(comment_tree)
                elif comment_tree:
                    tree["replies"].append(comment_tree)

        return tree

    def scrape_subreddit(self, subreddit_name, post_count):
        submission_list = []
        count = 1
        subreddit = self.reddit.subreddit(subreddit_name)

        for submission in subreddit.new(limit=post_count):
            print(f"Processing submission {count}/{post_count}")
            tree = self.with_rate_limit(self.create_submission_tree, submission)
            if tree:
                submission_list.append(tree)
            count += 1

        return submission_list

def main():
    POST_COUNT = 2000

    # Load credentials
    with open("client_secret.json") as secret_file:
        secret = json.load(secret_file)
        client_secret = secret["client_secret"]
        client_id = secret["client_id"]
        user_agent = secret["user_agent"]

    # Initialize scraper
    scraper = RedditScraper(client_id, client_secret, user_agent)

    # Perform scraping
    try:
        submission_list = scraper.scrape_subreddit("umass", POST_COUNT)

        # Save results
        with open("output.json", "w") as output_file:
            json.dump(submission_list, output_file, indent=4)

        print("Scraping completed successfully!")

    except Exception as e:
        print(f"An error occurred during scraping: {e}")

if __name__ == "__main__":
    main()
