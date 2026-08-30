import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieval.vector_search import search as vector_search
from retrieval.bm25 import search as bm25_search
from retrieval.rrf import reciprocal_rank_fusion
from retrieval.reranker import rerank
from retrieval.domain_gate import is_legal_query

def retrieve(query, vector_top_k=20, bm25_top_k=20, final_top_k=5):
    """
    Run the complete hybrid retrieval pipeline.
    """

    # 1. Check whether the question is related to the legal corpus
    is_legal, score = is_legal_query(query)

    if not is_legal:
        print(f"Query rejected. Qdrant score: {score:.4f}")
        return []

    # 2. Search Qdrant
    vector_results = vector_search(query, top_k=vector_top_k)

    # 3. Search BM25
    bm25_results = bm25_search(query, top_k=bm25_top_k)

    # 4. Combine both rankings using RRF
    rrf_results = reciprocal_rank_fusion(
        vector_results,
        bm25_results
    )

    # 5. Re-rank the combined results
    final_results = rerank(
        query,
        rrf_results,
        top_k=final_top_k
    )

    return final_results


if __name__ == "__main__":

    query = input("Enter your legal question: ")

    results = retrieve(query)

    if not results:
        print("\nThis question is outside the scope of the legal documents.")
    else:
        print("\nFinal Results:\n")

        for i, result in enumerate(results, start=1):

            chunk = result["chunk"]

            print(f"Rank: {i}")
            print(f"Score: {result['score']:.4f}")
            print(f"Source: {chunk['source']}")
            print(f"Part: {chunk['part_number']}")
            print(f"Chapter: {chunk['chapter_number']}")
            print(f"Section: {chunk['section_number']}")
            print(f"Title: {chunk['section_title']}")
            print(f"Text: {chunk['text'][:500]}...")
            print("-" * 60)