import os
from dotenv import load_dotenv
from retrieval.vector_search import search as vector_search
load_dotenv()


DOMAIN_THRESHOLD = float(os.getenv("DOMAIN_THRESHOLD", "0.50"))


def is_legal_query(query):
    """
    Check whether the question is relevant to the legal corpus.
    """

    results = vector_search(query,top_k=1)

    if not results:
        return False, 0.0
    best_score = results[0].score
    return best_score >= DOMAIN_THRESHOLD, best_score


if __name__ == "__main__":

    query = input("Enter your question: ")
    legal, score = is_legal_query(query)
    print(f"\nBest Qdrant score: {score:.4f}")
    if legal:
        print("Legal query: YES")
    else:
        print("Legal query: NO")