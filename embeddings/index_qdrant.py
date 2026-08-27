from pathlib import Path
import json
import os

import numpy as np
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models


# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "legal_documents"

CHUNKS_FILE = Path("data/chunks/chunks.jsonl")
EMBEDDINGS_FILE = Path("data/chunks/embeddings.npy")


def main():
    if not QDRANT_URL:
        raise ValueError("QDRANT_URL is missing from .env")

    if not QDRANT_API_KEY:
        raise ValueError("QDRANT_API_KEY is missing from .env")

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(f"Missing file: {CHUNKS_FILE}")

    if not EMBEDDINGS_FILE.exists():
        raise FileNotFoundError(f"Missing file: {EMBEDDINGS_FILE}")

    # --------------------------------------------------------
    # Connect to Qdrant Cloud
    # --------------------------------------------------------

    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )

    # --------------------------------------------------------
    # Load chunks
    # --------------------------------------------------------

    chunks = []

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    # --------------------------------------------------------
    # Load embeddings
    # --------------------------------------------------------

    embeddings = np.load(EMBEDDINGS_FILE)

    # --------------------------------------------------------
    # Basic validation
    # --------------------------------------------------------

    if len(chunks) != len(embeddings):
        raise ValueError(
            f"Chunk count ({len(chunks)}) does not match "
            f"embedding count ({len(embeddings)})"
        )

    vector_size = embeddings.shape[1]

    print(f"Chunks: {len(chunks)}")
    print(f"Embeddings: {embeddings.shape}")

    # --------------------------------------------------------
    # Create collection if it doesn't exist
    # --------------------------------------------------------

    collections = client.get_collections().collections

    collection_names = [collection.name for collection in collections]

    if COLLECTION_NAME not in collection_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE
            )
        )

        print(f"Created collection: {COLLECTION_NAME}")

    else:
        print(f"Collection already exists: {COLLECTION_NAME}")

    # --------------------------------------------------------
    # Create Qdrant points
    # --------------------------------------------------------

    points = []

    for i, chunk in enumerate(chunks):
        points.append(
            models.PointStruct(
                id=i,
                vector=embeddings[i].tolist(),
                payload=chunk
            )
        )

    # --------------------------------------------------------
    # Upload points to Qdrant
    # --------------------------------------------------------

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Uploaded {len(points)} points to Qdrant Cloud")


if __name__ == "__main__":
    main()