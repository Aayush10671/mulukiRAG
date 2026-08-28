from sentence_transformers import CrossEncoder


# ------------------------------------------------------------
# Reranker model
# ------------------------------------------------------------

MODEL_NAME = "BAAI/bge-reranker-base"

model = CrossEncoder(MODEL_NAME)


def rerank(query, results, top_k=5):
    """
    Re-rank retrieved chunks using a CrossEncoder.

    query:
        User's question

    results:
        Results returned by RRF

    top_k:
        Number of final chunks to keep
    """

    pairs = []

    for result in results:
        chunk = result["chunk"]
        pairs.append((query, chunk["text"]))

    # Score every (query, chunk) pair
    scores = model.predict(pairs)

    reranked_results = []

    for result, score in zip(results, scores):
        reranked_results.append({
            "score": float(score),
            "chunk": result["chunk"]
        })

    # Highest score first
    reranked_results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return reranked_results[:top_k]


# ------------------------------------------------------------
# Simple test
# ------------------------------------------------------------

if __name__ == "__main__":

    query = input("Enter your legal question: ")

    print("\nReranker is ready.")
    print("It needs RRF results before it can rerank them.")