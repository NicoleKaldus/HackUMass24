import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from pymongo import MongoClient
import json

# Load environment variables from .env file
load_dotenv()

# Access credentials
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
print(username, password)


uri = f"mongodb+srv://{username}:{password}@cluster0.lpgru.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client['hackathon_db']
collection = db['sam_data']


""" with open('output.json', 'r') as file:
    scraped_data = json.load(file)

collection.insert_many(scraped_data)
print("Data inserted successfully") """

""" scraped_data = {
    "title": "Example Article Title",
    "content": "Full text of the article goes here...",
    "source": "https://example.com/article-url",
    "metadata": {
        "author": "Author Name",
        "keywords": ["example", "data", "scraping"]
    }
}

collection.insert_one(scraped_data) """


""" with open('website_content.json', 'r') as file:
    sam_data = json.load(file)
collection.insert_many(sam_data)
print("Sam data inserted successfully") """

# Query data (e.g., retrieve all records)
documents = collection.find()

# Process data for model input
for doc in documents:
    content = doc
    print(content)
    # Apply preprocessing here if needed (e.g., tokenization, cleaning)
    # Pass processed content to OpenAI model
