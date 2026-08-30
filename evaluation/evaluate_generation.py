import json
import os
import sys
import time

# -------------------------------------------------------
# Allow imports from project root
# -------------------------------------------------------

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from qa_pipeline import answer_question

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

GOLDEN_PATH = "evaluation/golden.jsonl"

RESULTS_FOLDER = "evaluation/results"

REPORT_PATH = os.path.join(
    RESULTS_FOLDER,
    "generation_report.json"
)

# -------------------------------------------------------
# Load Golden Dataset
# -------------------------------------------------------

def load_golden_dataset():

    dataset = []

    with open(GOLDEN_PATH, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            dataset.append(json.loads(line))

    return dataset


# -------------------------------------------------------
# Source Evaluation
# -------------------------------------------------------

def evaluate_sources(
    predicted_sources,
    expected_sources
):
    """
    Returns True if any expected source appears
    in the predicted sources.
    """

    if predicted_sources is None:
        return False

    for expected in expected_sources:

        for predicted in predicted_sources:

            if (
                predicted["source"] == expected["source"]
                and str(predicted["section_number"])
                == str(expected["section_number"])
            ):
                return True

    return False


# -------------------------------------------------------
# Citation Evaluation
# -------------------------------------------------------

def evaluate_citations(citation_result):
    """
    Returns 1 if citation verification passed.
    """

    if citation_result is None:
        return 0

    return 1 if citation_result.get("valid", False) else 0


# -------------------------------------------------------
# Call QA pipeline with retry
# -------------------------------------------------------

def generate_with_retry(question, max_retries=3):
    """
    Retries automatically when NVIDIA returns 429.
    """

    for attempt in range(max_retries):

        try:
            return answer_question(question)

        except Exception as e:

            error_message = str(e)

            if "429" in error_message:

                wait_time = (attempt + 1) * 10

                print(
                    f"Rate limit reached. Waiting {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise

    raise Exception("Maximum retry attempts exceeded.")


# -------------------------------------------------------
# Main Evaluation
# -------------------------------------------------------

def evaluate():

    golden_data = load_golden_dataset()

    total_questions = len(golden_data)

    correct_answers = 0
    correct_citations = 0

    detailed_results = []

    print("=" * 70)
    print("GENERATION EVALUATION")
    print("=" * 70)

    for index, sample in enumerate(golden_data, start=1):

        question = sample["question"]
        expected_sources = sample["expected_sources"]

        print(f"\nQuestion {index}: {question}")

        try:

            result = generate_with_retry(question)

            source_correct = evaluate_sources(
                result.get("sources"),
                expected_sources
            )

            citation_correct = evaluate_citations(
                result.get("citation_check")
            )

            if source_correct:
                correct_answers += 1

            if citation_correct:
                correct_citations += 1

            detailed_results.append(
                {
                    "question": question,
                    "source_match": source_correct,
                    "citation_valid": bool(citation_correct),
                    "expected_sources": expected_sources,
                    "predicted_sources": result.get("sources", [])
                }
            )

            print(
                f"Source Match : {'YES' if source_correct else 'NO'}"
            )

            # Prevent NVIDIA rate limiting
            time.sleep(2)

        except Exception as e:

            detailed_results.append(
                {
                    "question": question,
                    "error": str(e)
                }
            )

            print(f"Error : {e}")

    # ---------------------------------------------------
    # Calculate Metrics
    # ---------------------------------------------------

    answer_accuracy = (
        correct_answers / total_questions
    ) * 100

    citation_accuracy = (
        correct_citations / total_questions
    ) * 100

    # ---------------------------------------------------
    # Save Report
    # ---------------------------------------------------

    os.makedirs(
        RESULTS_FOLDER,
        exist_ok=True
    )

    report = {
        "total_questions": total_questions,
        "answer_accuracy": round(answer_accuracy, 2),
        "citation_accuracy": round(citation_accuracy, 2),
        "correct_answers": correct_answers,
        "correct_citations": correct_citations,
        "details": detailed_results
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
    print("Evaluation completed successfully.")
    print(f"Report saved to: {REPORT_PATH}")
    print("=" * 70)


# -------------------------------------------------------

if __name__ == "__main__":
    evaluate()