import re


# ------------------------------------------------------------
# Common prompt-injection patterns
# ------------------------------------------------------------

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"forget\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(all\s+)?previous\s+instructions",
    r"override\s+(all\s+)?instructions",
    r"you\s+are\s+now\s+",
    r"act\s+as\s+",
    r"pretend\s+you\s+are",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"show\s+(me\s+)?your\s+system\s+prompt",
    r"reveal\s+your\s+instructions",
]


def contains_injection(text):
    """
    Check whether text contains common prompt-injection patterns.
    """

    text = text.lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text):
            return True

    return False


def check_query(query):
    """
    Check the user's question for prompt injection.
    """

    if contains_injection(query):
        return False, "Possible prompt injection detected."

    return True, "Query passed."


def check_chunks(results):
    """
    Check retrieved chunks for suspicious instructions.
    """

    for result in results:

        chunk = result["chunk"]

        if contains_injection(chunk["text"]):
            return False, f"Possible injection found in {chunk['chunk_id']}."

    return True, "Retrieved chunks passed."


def validate_inputs(query, results):
    """
    Validate both the user query and retrieved chunks.
    """

    query_ok, query_message = check_query(query)

    if not query_ok:
        return False, query_message

    chunks_ok, chunks_message = check_chunks(results)

    if not chunks_ok:
        return False, chunks_message

    return True, "All inputs passed."