import json
import praw
import pandas as pd
import re
import pprint

POST_COUNT = 100 #number of posts to extract

with open("client_secret.json") as secret_file:
  secret = json.load(secret_file)
  client_secret = secret["client_secret"]
  client_id = secret["client_id"]
  user_agent = secret["user_agent"]

# print(client_id, client_secret, user_agent)

reddit_read_only = praw.Reddit(client_id=client_id,       client_secret=client_secret, user_agent=user_agent)

subreddit = reddit_read_only.subreddit("umass")

def clean_text(text):
    # Allow only letters, numbers, and spaces
    return re.sub(r"[^a-zA-Z0-9\s/?:\n.']", '', text)


def comment_tree(comment):
  pprint.pprint(vars(comment))
  tree = {"user": "",
          "text": comment.body,
          "replies" : []}
  if comment.author:
    tree["user"] = comment.author.name
  else:
    tree["user"] = "[deleted]"
  for reply in comment.replies:
    tree["replies"].append(comment_tree(reply))
  return tree


def create_submission_tree(submission):
  tree = {"user": submission.author.name,
          "title":submission.title,
          "text": submission.selftext,
          "replies" : []}
  #pprint.pprint(vars(submission))
  submission.comment_sort = "hot"
  for comment in submission.comments:
    tree["replies"].append(comment_tree(comment))
  return tree

submission_list = []
for submission in subreddit.hot(limit = POST_COUNT):
  tree = create_submission_tree(submission)
  submission_list.append(tree)

with open("output.json", "w") as output_file:
  json.dump(submission_list, output_file, indent = 4)
