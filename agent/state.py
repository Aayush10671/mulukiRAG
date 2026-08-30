from typing import TypedDict, List, Dict, Optional


class AgentState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    # -----------------------------
    # User Input
    # -----------------------------

    question: str
    rewritten_query: str

    # -----------------------------
    # Retrieval
    # -----------------------------

    strategy: str
    retrieved_chunks: List[Dict]
    is_relevant: bool

    # -----------------------------
    # Generation
    # -----------------------------

    answer: str
    sources: List[Dict]
    citation_check: Dict

    # -----------------------------
    # Agent Control
    # -----------------------------

    attempts: int
    error: Optional[str]