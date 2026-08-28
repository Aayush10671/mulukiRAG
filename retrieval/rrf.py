def reciprocal_rank_fusion(vector_results, bm25_results, k=60):
    """
    Combine vector search and BM25 results using RRF.
    """
    scores = {}
    chunks = {}
    # ----------------------------------------
    # Add vector search rankings
    # ----------------------------------------

    for rank, result in enumerate(vector_results, start=1):

        chunk = result.payload
        chunk_id = chunk["chunk_id"]

        score = 1 / (k + rank)

        scores[chunk_id] = scores.get(chunk_id, 0) + score
        chunks[chunk_id] = chunk
    # ----------------------------------------
    # Add BM25 rankings
    # ----------------------------------------
    for rank, result in enumerate(bm25_results, start=1):

        chunk = result["chunk"]
        chunk_id = chunk["chunk_id"]

        score = 1 / (k + rank)

        scores[chunk_id] = scores.get(chunk_id, 0) + score
        chunks[chunk_id] = chunk
    # ----------------------------------------
    # Sort by combined RRF score
    # ----------------------------------------
    ranked_results = sorted(scores.items(),key=lambda item: item[1],reverse=True)
    # ----------------------------------------
    # Return chunks with scores
    # ----------------------------------------

    results = []
    for chunk_id, score in ranked_results:
        results.append({"score": score,"chunk": chunks[chunk_id]})

    return results