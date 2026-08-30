from openai import OpenAI
from dotenv import load_dotenv
import os

# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

MODEL_NAME = "nvidia/nemotron-3-ultra-550b-a55b"

# ---------------------------------------------------------
# Strategy 1 : Original Query
# ---------------------------------------------------------

def rewrite_original(question: str) -> str:
    """
    Returns the user's original question.
    """

    return question


# ---------------------------------------------------------
# Strategy 2 : Step-Back Prompting
# ---------------------------------------------------------

def rewrite_step_back(question: str) -> str:
    """
    Convert a specific legal question into a broader legal concept
    to improve retrieval.
    """

    prompt = f"""
You are a legal retrieval assistant.

Rewrite the user's question into a broader legal search query.
Do NOT answer the question.
Return ONLY the rewritten query.

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.3,
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------------------------
# Strategy 3 : HyDE
# ---------------------------------------------------------

def rewrite_hyde(question: str) -> str:
    """
    Generate a short hypothetical legal paragraph that can be
    embedded for semantic retrieval.
    """

    prompt = f"""
You are a legal assistant.

Write one short hypothetical legal passage (60-100 words)
that would likely appear inside a Nepalese statute.

Do NOT mention that it is hypothetical.

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.3,
        max_tokens=150,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------------------------
# Strategy Router
# ---------------------------------------------------------

def apply_strategy(
    question: str,
    strategy: str = "original"
) -> str:
    """
    Selects and applies the requested query rewriting strategy.
    """

    strategy = strategy.lower()

    if strategy == "original":
        return rewrite_original(question)

    elif strategy == "step_back":
        return rewrite_step_back(question)

    elif strategy == "hyde":
        return rewrite_hyde(question)

    else:
        raise ValueError(
            f"Unknown strategy: {strategy}"
        )


# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------

if __name__ == "__main__":

    question = input("Enter a legal question: ")

    print("\nOriginal")
    print("-" * 40)
    print(apply_strategy(question, "original"))

    print("\nStep-Back")
    print("-" * 40)
    print(apply_strategy(question, "step_back"))

    print("\nHyDE")
    print("-" * 40)
    print(apply_strategy(question, "hyde"))