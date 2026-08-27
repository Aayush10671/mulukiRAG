# from pathlib import Path
# import json
# import numpy as np
# from sentence_transformers import SentenceTransformer

# CHUNKS_FILE = Path("data/chunks/chunks.jsonl")
# OUTPUT_FILE = Path("data/chunks/embeddings.npy")

# MODEL_NAME = "BAAI/bge-small-en-v1.5"


# def main():
#     model = SentenceTransformer(MODEL_NAME)

#     chunks = []

#     with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
#         for line in file:
#             chunks.append(json.loads(line))

#     texts = [chunk["text"] for chunk in chunks]

#     embeddings = model.encode(
#         texts,
#         normalize_embeddings=True,
#         show_progress_bar=True
#     )

#     np.save(OUTPUT_FILE, embeddings)

#     print(f"Created embeddings: {embeddings.shape}")
#     print(f"Saved to: {OUTPUT_FILE}")


# if __name__ == "__main__":
#     main()


from pathlib import Path
import json
import numpy as np
from model import embed_documents

CHUNKS_FILE = Path("data/chunks/chunks.jsonl")
OUTPUT_FILE = Path("data/chunks/embeddings.npy")


def main():
    chunks = []

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    texts = [chunk["text"] for chunk in chunks]

    embeddings = embed_documents(texts)

    np.save(OUTPUT_FILE, embeddings)

    print(f"Created embeddings: {embeddings.shape}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()