import re
def get_citations(answer):
    """
    Find citation tags such as [S1], [S2], [S3].
    """
    return re.findall(r"\[S\d+\]", answer)

def verify_citations(answer, results):
    """
    Check whether every citation in the answer refers
    to a retrieved chunk.
    """
    citations = get_citations(answer)
    valid_citations = {f"[S{i}]"for i in range(1, len(results) + 1)}

    invalid_citations = [citation for citation in citations if citation not in valid_citations]

    return {"valid": len(invalid_citations) == 0, "citations": citations,"invalid_citations": invalid_citations}

def add_sources(answer, results):
    """
    Add the source details for the citations used in the answer.
    """
    citations = get_citations(answer)
    sources = []
    for citation in citations:
        index = int(citation[2:-1]) - 1
        if 0 <= index < len(results):
            chunk = results[index]["chunk"]
            sources.append({
                "citation": citation,
                "source": chunk["source"],
                "part_number": chunk["part_number"],
                "part_title": chunk["part_title"],
                "chapter_number": chunk["chapter_number"],
                "chapter_title": chunk["chapter_title"],
                "section_number": chunk["section_number"],
                "section_title": chunk["section_title"]
            })
    return sources


if __name__ == "__main__":

    answer = """
    The relevant provision provides for compensation to the victim. [S1]
    The limitation period is also specified by law. [S2]
    """

    results = [
        {
            "chunk": {
                "source": "National-Penal-Code",
                "part_number": "2",
                "part_title": "Criminal Offences",
                "chapter_number": "9",
                "chapter_title": "Offences Relating to Religion",
                "section_number": "169",
                "section_title": "Order for compensation to be paid"
            }
        },
        {
            "chunk": {
                "source": "Domestic-Violence-Act",
                "part_number": None,
                "part_title": None,
                "chapter_number": None,
                "chapter_title": None,
                "section_number": "14",
                "section_title": "Limitation"
            }
        }
    ]

    result = verify_citations(answer, results)
    print("Citation check:")
    print(result)
    print("\nSources:")
    print(add_sources(answer, results))