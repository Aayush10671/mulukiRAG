from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"

model = SentenceTransformer(MODEL_NAME)


def embed_documents(texts):
    return model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )


def embed_query(text):
    return model.encode(
        text,
        normalize_embeddings=True
    )