import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.nodes import (
    rewrite_node,
    retrieve_node,
    grade_node,
    generate_node,
    verify_node,
    retry_node
)

# ---------------------------------------------------------
# Decide where to go after grading
# ---------------------------------------------------------

MAX_RETRIES = 2


def route_after_grade(state: AgentState):
    """
    If retrieval is good → Generate.
    Otherwise retry until MAX_RETRIES.
    """

    if state["is_relevant"]:
        return "generate"

    if state["attempts"] >= MAX_RETRIES:
        return "generate"

    return "retry"


# ---------------------------------------------------------
# Build Graph
# ---------------------------------------------------------

builder = StateGraph(AgentState)

# Nodes
builder.add_node("rewrite", rewrite_node)
builder.add_node("retrieve", retrieve_node)
builder.add_node("grade", grade_node)
builder.add_node("retry", retry_node)
builder.add_node("generate", generate_node)
builder.add_node("verify", verify_node)

# Entry point
builder.set_entry_point("rewrite")

# Edges
builder.add_edge("rewrite", "retrieve")
builder.add_edge("retrieve", "grade")

builder.add_conditional_edges(
    "grade",
    route_after_grade,
    {
        "generate": "generate",
        "retry": "retry"
    }
)

builder.add_edge("retry", "rewrite")
builder.add_edge("generate", "verify")
builder.add_edge("verify", END)

# Compile
legal_agent = builder.compile()


# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------

if __name__ == "__main__":

    question = input("Enter your legal question: ")

    initial_state = {
        "question": question,
        "rewritten_query": "",
        "strategy": "step_back",
        "retrieved_chunks": [],
        "is_relevant": False,
        "answer": "",
        "sources": [],
        "citation_check": {},
        "attempts": 0,
        "error": None
    }

    result = legal_agent.invoke(initial_state)

    print("\nAnswer\n")
    print(result["answer"])

    print("\nSources\n")
    for source in result["sources"]:
        print(
            f"{source['citation']} | "
            f"{source['source']} | "
            f"Section {source['section_number']}"
        )