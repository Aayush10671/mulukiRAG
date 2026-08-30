import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pathlib import Path

from retrieval.pipeline import retrieve


GOLDEN_FILE = Path("evaluation/golden.jsonl")


def load_golden_data():
    data = []
    with open(GOLDEN_FILE, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data.append(json.loads(line))
    return data


def source_matches(chunk, expected_source):
    """
    Check whether a retrieved chunk matches an expected source.
    """

    return (
        chunk["source"] == expected_source["source"]
        and str(chunk["section_number"])
        == str(expected_source["section_number"])
    )


def is_hit(results, expected_sources, k):
    """
    Check whether any expected source appears in the top-k results.
    """

    top_results = results[:k]

    for result in top_results:

        chunk = result["chunk"]

        for expected_source in expected_sources:

            if source_matches(chunk, expected_source):
                return True

    return False


def evaluate():
    """
    Evaluate the retrieval pipeline using golden.jsonl.
    """

    questions = load_golden_data()

    total_questions = len(questions)

    hit_at_1 = 0
    hit_at_3 = 0
    hit_at_5 = 0

    print(f"Total questions: {total_questions}")
    print("-" * 70)

    for number, item in enumerate(questions, start=1):

        question = item["question"]
        expected_sources = item["expected_sources"]

        print(f"\nQuestion {number}: {question}")

        results = retrieve(
            question,
            vector_top_k=30,
            bm25_top_k=30,
            final_top_k=5
        )

        if not results:
            print("No results returned.")
            continue

        if is_hit(results, expected_sources, 1):
            hit_at_1 += 1

        if is_hit(results, expected_sources, 3):
            hit_at_3 += 1

        if is_hit(results, expected_sources, 5):
            hit_at_5 += 1

        print("Top results:")

        for rank, result in enumerate(results, start=1):

            chunk = result["chunk"]

            print(
                f"  {rank}. "
                f"{chunk['source']} - "
                f"Section {chunk['section_number']}"
            )

    # --------------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------------

    hit_at_1_score = hit_at_1 / total_questions
    hit_at_3_score = hit_at_3 / total_questions
    hit_at_5_score = hit_at_5 / total_questions

    print("\n" + "=" * 70)
    print("EVALUATION RESULTS")
    print("=" * 70)

    print(f"Hit@1: {hit_at_1_score:.2%}")
    print(f"Hit@3: {hit_at_3_score:.2%}")
    print(f"Hit@5: {hit_at_5_score:.2%}")


if __name__ == "__main__":
    evaluate()