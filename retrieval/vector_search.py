import sys
import os
import streamlit as st
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from embeddings.model import embed_query


# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL") or st.secrets["QDRANT_URL"]
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or st.secrets["QDRANT_API_KEY"]
COLLECTION_NAME = "legal_documents"


# ------------------------------------------------------------
# Connect to Qdrant
# ------------------------------------------------------------

client = QdrantClient(url=QDRANT_URL,api_key=QDRANT_API_KEY)

def search(query, top_k=5):
    """
    Search Qdrant for the most similar legal chunks.
    """

    query_vector = embed_query(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector.tolist(),
        limit=top_k,
        with_payload=True
    ).points
    print("searched into qdrant")

    return results

# ------------------------------------------------------------
# Test
# ------------------------------------------------------------

if __name__ == "__main__":

    query = input("Enter your legal question: ")

    results = search(query)

    for result in results:

        payload = result.payload

        print()
        print(f"Score: {result.score}")
        print(f"Source: {payload['source']}")
        print(f"Part: {payload['part_number']}")
        print(f"Chapter: {payload['chapter_number']}")
        print(f"Section: {payload['section_number']}")
        print(f"Title: {payload['section_title']}")
        print(f"Text: {payload['text'][:1000]}...")