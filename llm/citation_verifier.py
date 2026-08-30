import re
CITATION_PATTERN = re.compile(r"\[S(\d+)\]")
def get_citations(answer):
    """
    Extract citations such as [S1], [S2], [S3].
    """
    return CITATION_PATTERN.findall(answer)


def verify_citations(answer, results):
    """
    Verify that every citation in the answer points to
    one of the retrieved chunks.
    """
    citation_numbers = get_citations(answer)

    valid_citations = []
    invalid_citations = []

    for number in citation_numbers:

        index = int(number) - 1

        if 0 <= index < len(results):
            valid_citations.append(f"[S{number}]")
        else:
            invalid_citations.append(f"[S{number}]")

    return {
        "valid": len(invalid_citations) == 0,
        "citations_found": list(dict.fromkeys(
            f"[S{number}]" for number in citation_numbers
        )),
        "valid_citations": list(dict.fromkeys(valid_citations)),
        "invalid_citations": list(dict.fromkeys(invalid_citations))
    }


def get_citation_sources(answer, results):
    """
    Get the exact legal source information for every
    valid citation used in the answer.
    """

    citation_numbers = get_citations(answer)

    sources = []
    seen = set()

    for number in citation_numbers:

        index = int(number) - 1

        if not (0 <= index < len(results)):
            continue

        chunk = results[index]["chunk"]

        citation = f"[S{number}]"

        if citation in seen:
            continue

        seen.add(citation)

        sources.append({
            "citation": citation,
            "chunk_id": chunk["chunk_id"],
            "source": chunk["source"],
            "part_number": chunk["part_number"],
            "part_title": chunk["part_title"],
            "chapter_number": chunk["chapter_number"],
            "chapter_title": chunk["chapter_title"],
            "section_number": chunk["section_number"],
            "section_title": chunk["section_title"],
            "text": chunk["text"]
        })

    return sources


def verify_and_get_sources(answer, results):
    """
    Verify citations and return their exact legal sources.
    """
    verification = verify_citations(answer,results)

    sources = get_citation_sources(answer,results)

    return {**verification,"sources": sources}