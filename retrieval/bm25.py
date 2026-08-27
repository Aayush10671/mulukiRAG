from pathlib import Path
import json
import re

from rank_bm25 import BM25Okapi

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHUNKS_FILE = Path("data/chunks/chunks.jsonl")

def load_chunks():
    """Load all legal chunks from chunks.jsonl."""
    chunks = []

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))
    return chunks


def tokenize(text):
    """Convert text into simple lowercase tokens."""
    return re.findall(r"\b\w+\b", text.lower())


def create_bm25_index(chunks):
    """Create a BM25 index from the chunk text."""
    tokenized_texts = [
        tokenize(chunk["text"])
        for chunk in chunks
    ]

    return BM25Okapi(tokenized_texts)


def search(query, top_k=5):
    """Return the top-k chunks using BM25."""

    chunks = load_chunks()
    bm25 = create_bm25_index(chunks)
    query_tokens = tokenize(query)
    scores = bm25.get_scores(query_tokens)
    top_indices = scores.argsort()[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append({
            "score": float(scores[index]),
            "chunk": chunks[index]
        })

    return results

if __name__ == "__main__":

    query = input("Enter your legal question: ")
    results = search(query)
    for result in results:

        chunk = result["chunk"]

        print()
        print(f"Score: {result['score']:.4f}")
        print(f"Source: {chunk['source']}")
        print(f"Part: {chunk['part_number']}")
        print(f"Chapter: {chunk['chapter_number']}")
        print(f"Section: {chunk['section_number']}")
        print(f"Title: {chunk['section_title']}")
        print(f"Text: {chunk['text'][:500]}...")