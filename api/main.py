from fastapi import FastAPI
from pydantic import BaseModel

from qa_pipeline import answer_question

# ---------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------

app = FastAPI(
    title="Nepal Legal RAG API",
    description="Hybrid Legal Question Answering System for Nepalese Law",
    version="1.0.0"
)

# ---------------------------------------------------------
# Request Schema
# ---------------------------------------------------------

class QueryRequest(BaseModel):
    question: str


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Nepal Legal RAG API is running."
    }


# ---------------------------------------------------------
# Query Endpoint
# ---------------------------------------------------------

@app.post("/query")
def query(request: QueryRequest):
    """
    Main endpoint for legal question answering.
    """

    try:
        result = answer_question(request.question)

        return {
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"],
            "citation_check": result["citation_check"]
        }

    except Exception as e:
        return {
            "question": request.question,
            "answer": "An internal error occurred while processing your question.",
            "sources": [],
            "citation_check": {
                "valid": False,
                "error": str(e)
            }
        }


# ---------------------------------------------------------
# Trace Endpoint
# ---------------------------------------------------------

@app.post("/trace")
def trace(request: QueryRequest):
    """
    Returns the complete pipeline output.
    Useful for debugging and evaluation.
    """

    try:
        return answer_question(request.question)

    except Exception as e:
        return {
            "answer": "",
            "sources": [],
            "citation_check": {
                "valid": False,
                "error": str(e)
            }
        }


# from fastapi import FastAPI
# from pydantic import BaseModel

# from qa_pipeline import answer_question

# # ---------------------------------------------------------
# # FastAPI App
# # ---------------------------------------------------------

# app = FastAPI(
#     title="Nepal Legal RAG API",
#     description="Agentic Hybrid Legal Question Answering System",
#     version="1.0.0"
# )

# # ---------------------------------------------------------
# # Request Schema
# # ---------------------------------------------------------

# class QueryRequest(BaseModel):
#     question: str
#     strategy: str = "step_back"


# # ---------------------------------------------------------
# # Health Check
# # ---------------------------------------------------------

# @app.get("/")
# def home():
#     return {
#         "message": "Nepal Legal RAG API is running."
#     }


# # ---------------------------------------------------------
# # Query Endpoint
# # ---------------------------------------------------------

# @app.post("/query")
# def query(request: QueryRequest):

#     try:
#         result = answer_question(
#             query=request.question,
#             strategy=request.strategy
#         )

#         return {
#             "question": request.question,
#             "strategy": request.strategy,
#             "answer": result["answer"],
#             "sources": result["sources"],
#             "citation_check": result["citation_check"]
#         }

#     except Exception as e:

#         return {
#             "question": request.question,
#             "strategy": request.strategy,
#             "answer": "An internal error occurred while processing your question.",
#             "sources": [],
#             "citation_check": {
#                 "valid": False,
#                 "error": str(e)
#             }
#         }


# # ---------------------------------------------------------
# # Trace Endpoint
# # ---------------------------------------------------------

# @app.post("/trace")
# def trace(request: QueryRequest):
#     """
#     Debug endpoint for the agent.
#     Returns the complete pipeline output.
#     """

#     try:
#         return answer_question(
#             query=request.question,
#             strategy=request.strategy
#         )

#     except Exception as e:

#         return {
#             "answer": "",
#             "sources": [],
#             "citation_check": {
#                 "valid": False,
#                 "error": str(e)
#             }
#         }