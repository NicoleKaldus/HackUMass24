import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from pymongo import MongoClient
import openai


# Load environment variables from .env file
load_dotenv()

# Access credentials
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")

uri = f"mongodb+srv://{username}:{password}@cluster0.lpgru.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# Create a new client and connect to the server
client = MongoClient(uri)


db = client["hackathon_db"]
collection = db["goose2"]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
from openai import OpenAI

AIclient = OpenAI(api_key=OPENAI_API_KEY)

def generate_query_embedding(query):

    response = AIclient.embeddings.create(input=query, model="text-embedding-3-small")
    print(response)
    return response.data[0].embedding


# Example usage
query = "How does MongoDB handle vector indexing for semantic search?"
query_embedding = generate_query_embedding(query)


def search_most_relevant_answers(query_embedding, top_k=5):
    pipeline = [
        {
            "$search": {
                "knnBeta": {
                    "vector": query_embedding,
                    "path": "embedding",
                    "k": top_k
                }
            }
        },
        {
            "$project": {
                "text": 1,
                "score": {"$meta": "searchScore"}
            }
        }
    ]
    results = list(collection.aggregate(pipeline))
    print(results)
    return results

# Execute search
top_results = search_most_relevant_answers(query_embedding)

def extract_text_from_results(results):
    text_snippets = [result['text'] for result in results]
    return " ".join(text_snippets)

# Aggregate relevant text
combined_text = extract_text_from_results(top_results)

def synthesize_answer(combined_text, query):
    prompt = f"Given the following information:\n\n{combined_text}\n\nAnswer the question: '{query}' in a concise and definitive manner."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content']

# Get a synthesized answer
final_answer = synthesize_answer(combined_text, query)
print("Definitive Answer:", final_answer)
