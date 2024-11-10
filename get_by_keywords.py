import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from pymongo import MongoClient


# Load environment variables from .env file
load_dotenv()

# Access credentials
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")

uri = f"mongodb+srv://{username}:{password}@cluster0.lpgru.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["hackathon_db"]


def ask_goose_by_keywords(keywords):
    # keywords is a list of keywords that are relevant to the query
    collection = db["goose_data"]
    if (
        "text_text" not in collection.list_indexes()
    ):  # 'text_text' is the default name for a text index on the 'text' field
        collection.create_index([("text", "text")])
    for i in collection.list_indexes():
        print(i)
    # Perform a text search to find documents containing the keyword in the "content" field
    ret = {}
    appended_posts = (
        set()
    )  # make sure that each post can only be appended once for faster AI processing
    for k in keywords:
        ret[k] = []  # create
        query = {"$text": {"$search": k}}
        documents = collection.find(query)
        count = 0
        for doc in documents:
            content = doc
            if not content["_id"] in appended_posts:
                ret[k].append(content)
                appended_posts.add(content["_id"])
            count += 1

        print(count, " documents found for keyword ", k)

    return ret


def ask_sam_by_keywords(keywords):
    # keywords is a list of keywords that are relevant to the query
    collection = db["sam_data"]
    if (
        "content_text" not in collection.list_indexes()
    ):  # 'text_text' is the default name for a text index on the 'text' field
        collection.create_index([("content", "text")])
    for i in collection.list_indexes():
        print(i)
    # Perform a text search to find documents containing the keyword in the "content" field
    ret = {}
    appended_posts = (
        set()
    )  # make sure that each post can only be appended once for faster AI processing
    for k in keywords:
        ret[k] = []  # create
        query = {"$text": {"$search": k}}
        documents = collection.find(query)
        count = 0
        for doc in documents:
            content = doc
            if not content["_id"] in appended_posts:
                ret[k].append(content)
                appended_posts.add(content["_id"])
            count += 1

        print(count, " documents found for keyword ", k)

    return ret


if __name__ == "__main__":
    goose_posts = ask_goose_by_keywords(["painting", "campus"])
    print(goose_posts)
    sam_posts = ask_sam_by_keywords(["important", "dorm"])
    print(sam_posts)
