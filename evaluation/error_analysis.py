import json
import os
import sys

# -------------------------------------------------------
# Allow imports from project root
# -------------------------------------------------------

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from retrieval.pipeline import retrieve

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

GOLDEN_PATH = "evaluation/golden.jsonl"

RESULTS_FOLDER = "evaluation/results"

REPORT_PATH = os.path.join(
    RESULTS_FOLDER,
    "error_analysis.json"
)

# -------------------------------------------------------
# Load golden dataset
# -------------------------------------------------------

def load_golden_dataset():

    dataset = []

    with open(GOLDEN_PATH, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if line:
                dataset.append(json.loads(line))

    return dataset


# -------------------------------------------------------
# Check if retrieved chunk matches expected chunk
# -------------------------------------------------------

def is_correct_result(
    results,
    expected_sources
):

    for result in results:

        chunk = result["chunk"]

        for expected in expected_sources:

            if (
                chunk["source"] == expected["source"]
                and str(chunk["section_number"])
                == str(expected["section_number"])
            ):
                return True

    return False


# -------------------------------------------------------
# Main analysis
# -------------------------------------------------------

def analyze():

    golden_data = load_golden_dataset()

    failed_questions = []

    total = len(golden_data)
    failed = 0

    print("=" * 70)
    print("RETRIEVAL ERROR ANALYSIS")
    print("=" * 70)

    for index, sample in enumerate(golden_data, start=1):

        question = sample["question"]
        expected = sample["expected_sources"]

        print(f"Question {index}")

        try:

            results = retrieve(
                question,
                vector_top_k=50,
                bm25_top_k=50,
                final_top_k=5
            )

            correct = is_correct_result(
                results,
                expected
            )

            if not correct:

                failed += 1

                retrieved = []

                for result in results:

                    chunk = result["chunk"]

                    retrieved.append(
                        {
                            "source": chunk["source"],
                            "section_number": chunk["section_number"],
                            "score": round(result["score"], 4)
                        }
                    )

                failed_questions.append(
                    {
                        "question": question,
                        "expected_sources": expected,
                        "retrieved": retrieved
                    }
                )

                print("FAILED")

            else:

                print("PASSED")

        except Exception as e:

            failed += 1

            failed_questions.append(
                {
                    "question": question,
                    "expected_sources": expected,
                    "error": str(e)
                }
            )

            print(f"ERROR : {e}")

    # ---------------------------------------------------
    # Save report
    # ---------------------------------------------------

    os.makedirs(
        RESULTS_FOLDER,
        exist_ok=True
    )

    report = {
        "total_questions": total,
        "failed_questions": failed,
        "passed_questions": total - failed,
        "details": failed_questions
    }

    with open(
        REPORT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 70)
    print("Analysis completed successfully.")
    print(f"Report saved to: {REPORT_PATH}")
    print("=" * 70)


# -------------------------------------------------------

if __name__ == "__main__":
    analyze()