from agent.state import AgentState
from agent.strategies import apply_strategy

from retrieval.pipeline import retrieve
from llm.generate import generate_answer
from llm.guardrails import validate_inputs
from llm.citation_verifier import verify_citations, get_citation_sources


# ---------------------------------------------------------
# Rewrite Node
# ---------------------------------------------------------

def rewrite_node(state: AgentState) -> AgentState:
    """
    Rewrite the user's question using the selected strategy.
    """

    rewritten_query = apply_strategy(
        question=state["question"],
        strategy=state["strategy"]
    )

    state["rewritten_query"] = rewritten_query

    return state


# ---------------------------------------------------------
# Retrieve Node
# ---------------------------------------------------------

def retrieve_node(state: AgentState) -> AgentState:
    """
    Run the hybrid retrieval pipeline.
    """

    results = retrieve(
        query=state["rewritten_query"],
        vector_top_k=20,
        bm25_top_k=20,
        final_top_k=5
    )

    state["retrieved_chunks"] = results

    return state


# ---------------------------------------------------------
# Grade Retrieval Node
# ---------------------------------------------------------

def grade_node(state: AgentState) -> AgentState:
    """
    Decide whether the retrieved chunks are relevant enough.
    """

    results = state["retrieved_chunks"]

    valid, _ = validate_inputs(
        state["question"],
        results
    )

    state["is_relevant"] = valid

    return state


# ---------------------------------------------------------
# Generate Node
# ---------------------------------------------------------

def generate_node(state: AgentState) -> AgentState:
    """
    Generate the final legal answer.
    """

    answer = generate_answer(
        query=state["question"],
        results=state["retrieved_chunks"]
    )

    state["answer"] = answer

    return state


# ---------------------------------------------------------
# Verify Citation Node
# ---------------------------------------------------------

def verify_node(state: AgentState) -> AgentState:
    """
    Verify citations and attach legal sources.
    """

    citation_result = verify_citations(
        state["answer"],
        state["retrieved_chunks"]
    )

    sources = get_citation_sources(
        state["answer"],
        state["retrieved_chunks"]
    )

    state["citation_check"] = citation_result
    state["sources"] = sources

    return state


# ---------------------------------------------------------
# Retry Node
# ---------------------------------------------------------

def retry_node(state: AgentState) -> AgentState:
    """
    Increase retry counter before another retrieval attempt.
    """

    state["attempts"] += 1

    return state