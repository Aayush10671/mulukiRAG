# from retrieval.pipeline import retrieve
# from llm.generate import generate_answer
# from llm.guardrails import validate_inputs
# from llm.citation_verifier import verify_and_get_sources

# def answer_question(query):

#     # --------------------------------------------------------
#     # 1. Retrieve relevant legal chunks
#     # --------------------------------------------------------

#     results = retrieve(query,vector_top_k=20,bm25_top_k=20,final_top_k=5)

#     if not results:
#         return {"answer": "I could not find relevant legal information.","sources": [],"citation_check": None}

#     # --------------------------------------------------------
#     # 2. Check query and retrieved chunks
#     # --------------------------------------------------------

#     valid, message = validate_inputs(query,results)

#     if not valid:
#         return {"answer": message,"sources": [],"citation_check": None}

#     # --------------------------------------------------------
#     # 3. Generate answer using Kimi K3
#     # --------------------------------------------------------

#     answer = generate_answer(query,results)

#     # --------------------------------------------------------
#     # 4. Verify citations and get source information
#     # --------------------------------------------------------

#     citation_result = verify_and_get_sources(answer,results)
#     sources = citation_result["sources"]

#     # --------------------------------------------------------
#     # 5. Warn if citation is invalid
#     # --------------------------------------------------------

#     if not citation_result["valid"]:

#         answer += (
#             "\n\nWarning: Some citations could not be verified."
#         )

#     # --------------------------------------------------------
#     # 6. Return final result
#     # --------------------------------------------------------

#     return {
#         "answer": answer,
#         "sources": sources,
#         "citation_check": citation_result
#     }


# # ============================================================
# # TEST
# # ============================================================

# if __name__ == "__main__":

#     question = input("Enter your legal question: ")

#     result = answer_question(question)

#     print("\nAnswer:")
#     print(result["answer"])

#     print("\nSources:")

#     for source in result["sources"]:

#         print(
#             f"{source['citation']} - "
#             f"{source['source']} - "
#             f"Section {source['section_number']} - "
#             f"{source['section_title']}"
#         )

#     print("\nCitation Check:")
#     print(result["citation_check"])


from agent.graph import legal_agent


def answer_question(
    query: str,
    strategy: str = "step_back"
):
    """
    Entry point for the Agentic Legal RAG.
    """

    initial_state = {
        "question": query,
        "rewritten_query": "",
        "strategy": strategy,
        "retrieved_chunks": [],
        "is_relevant": False,
        "answer": "",
        "sources": [],
        "citation_check": {},
        "attempts": 0,
        "error": None
    }

    result = legal_agent.invoke(initial_state)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "citation_check": result["citation_check"]
    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    question = input("Enter your legal question: ")

    result = answer_question(question)

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nSources:\n")

    for source in result["sources"]:
        print(
            f"{source['citation']} | "
            f"{source['source']} | "
            f"Section {source['section_number']} | "
            f"{source['section_title']}"
        )

    print("\nCitation Check:\n")
    print(result["citation_check"])