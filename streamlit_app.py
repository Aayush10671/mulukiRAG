# import streamlit as st
# import requests

# # ---------------------------------------------------------
# # Configuration
# # ---------------------------------------------------------

# st.set_page_config(
#     page_title="मुलुकी RAG | Nepal Legal Assistant",
#     page_icon="⚖️",
#     layout="wide"
# )

# API_URL = "http://127.0.0.1:8000/query"

# CRIMSON = "#DC143C"
# NAVY = "#003893"

# # ---------------------------------------------------------
# # Light touch of theme — just red/blue accents, nothing heavy
# # ---------------------------------------------------------

# st.markdown(f"""
# <style>
# .accent-bar {{
#     height: 4px;
#     width: 130px;
#     background: linear-gradient(90deg, {CRIMSON} 50%, {NAVY} 50%);
#     border-radius: 2px;
#     margin: 6px 0 22px 0;
# }}

# .mrag-card {{
#     background: #ffffff;
#     border-radius: 10px;
#     padding: 1.2rem 1.4rem;
#     border: 1px solid #eee;
#     margin-bottom: 1rem;
# }}
# .mrag-answer-card {{ border-left: 4px solid {NAVY}; }}

# .stButton > button {{
#     background: {CRIMSON};
#     color: white;
#     border: none;
#     border-radius: 8px;
#     font-weight: 600;
# }}
# .stButton > button:hover {{ background: {NAVY}; color: white; }}

# div[data-testid="stSidebar"] .stButton > button {{
#     background: #ffffff;
#     color: {NAVY};
#     border: 1px solid {NAVY};
#     text-align: left;
#     font-weight: 500;
#     font-size: 0.85rem;
#     white-space: normal;
# }}
# div[data-testid="stSidebar"] .stButton > button:hover {{
#     background: {NAVY};
#     color: white;
# }}

# div[data-testid="stExpander"] {{
#     border-left: 3px solid {CRIMSON};
#     border-radius: 8px;
# }}
# </style>
# """, unsafe_allow_html=True)

# # ---------------------------------------------------------
# # Header
# # ---------------------------------------------------------

# st.title("⚖️ मुलुकी RAG — Nepal Legal Assistant")
# st.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)
# st.markdown(
#     "Ask questions about Nepalese law — Muluki Criminal Code, Civil Code, "
#     "and the Domestic Violence Act — powered by Hybrid Retrieval-Augmented Generation."
# )
# st.caption("धर्मो रक्षति रक्षितः — कानूनी प्रश्नहरूको भरपर्दो उत्तर")

# # ---------------------------------------------------------
# # Sidebar — example questions
# # ---------------------------------------------------------

# if "question" not in st.session_state:
#     st.session_state.question = ""

# with st.sidebar:
#     st.markdown("### About")
#     st.caption(
#         "मुलुकी RAG retrieves relevant provisions from Nepal's Muluki "
#         "Criminal Code, Civil Code, and Domestic Violence Act, then "
#         "generates a cited legal answer."
#     )
#     st.markdown("### Try an example")
#     examples = [
#         "When can a prisoner be placed on parole?",
#         "What constitutes domestic violence under Nepali law?",
#         "What is the punishment for theft under the Muluki Criminal Code?",
#         "What are the grounds for divorce under the Civil Code?",
#     ]
#     for ex in examples:
#         if st.button(ex, key=ex, use_container_width=True):
#             st.session_state.question = ex
#             st.rerun()

# # ---------------------------------------------------------
# # User Input
# # ---------------------------------------------------------

# question = st.text_area(
#     "Enter your legal question",
#     value=st.session_state.question,
#     height=150,
#     placeholder="Example: When can a prisoner be placed on parole?"
# )

# ask = st.button("Ask Question", type="primary", use_container_width=True)

# # ---------------------------------------------------------
# # Query
# # ---------------------------------------------------------

# if ask:

#     if question.strip() == "":
#         st.warning("Please enter a legal question.")
#         st.stop()

#     payload = {"question": question}

#     with st.spinner("Searching Nepalese law..."):
#         try:
#             response = requests.post(API_URL, json=payload, timeout=120)
#             response.raise_for_status()
#             result = response.json()

#         except requests.exceptions.ConnectionError:
#             st.error(
#                 "Cannot connect to the FastAPI server.\n\n"
#                 "Start it using:\n"
#                 "`uvicorn api.main:app --reload`"
#             )
#             st.stop()

#         except Exception as e:
#             st.error(f"Error: {e}")
#             st.stop()

#     # -----------------------------------------------------
#     # Answer
#     # -----------------------------------------------------

#     st.markdown('<div class="mrag-card mrag-answer-card">', unsafe_allow_html=True)
#     st.markdown("#### 📖 Legal Answer")
#     st.write(result["answer"])
#     st.markdown('</div>', unsafe_allow_html=True)

#     # -----------------------------------------------------
#     # Sources
#     # -----------------------------------------------------

#     st.markdown("#### 📚 Cited Legal Sources")

#     sources = result.get("sources", [])

#     if len(sources) == 0:
#         st.info("No legal sources were returned.")
#     else:
#         for source in sources:
#             with st.expander(
#                 f"{source['citation']} • {source['source']} • Section {source['section_number']}"
#             ):
#                 st.markdown(f"**Section:** {source['section_number']}")
#                 st.markdown(f"**Title:** {source['section_title']}")
#                 st.markdown(f"**Source:** {source['source']}")

#     # -----------------------------------------------------
#     # Citation Verification
#     # -----------------------------------------------------

#     st.markdown("#### ✅ Citation Verification")

#     citation = result.get("citation_check")

#     if citation is None:
#         st.warning("Citation verification was not performed.")
#     elif citation.get("valid", False):
#         st.success("All citations were successfully verified.")
#     else:
#         st.error("Some citations could not be verified.")
#         if "error" in citation:
#             st.caption(citation["error"])

# # ---------------------------------------------------------
# # Footer
# # ---------------------------------------------------------

# st.markdown("---")
# st.caption("मुलुकी RAG · Muluki Criminal Code · Civil Code · Domestic Violence Act")


# import streamlit as st
# import requests

# # ---------------------------------------------------------
# # Configuration
# # ---------------------------------------------------------

# st.set_page_config(
#     page_title="मुलुकी RAG | Nepal Legal Assistant",
#     page_icon="⚖️",
#     layout="wide"
# )

# API_URL = "http://127.0.0.1:8000/query"

# CRIMSON = "#DC143C"
# NAVY = "#003893"

# # ---------------------------------------------------------
# # Styling
# # ---------------------------------------------------------

# st.markdown(f"""
# <style>
# .accent-bar {{
#     height: 4px;
#     width: 130px;
#     background: linear-gradient(90deg, {CRIMSON} 50%, {NAVY} 50%);
#     border-radius: 2px;
#     margin: 6px 0 22px 0;
# }}

# .mrag-card {{
#     background: #ffffff;
#     border-radius: 10px;
#     padding: 1.2rem 1.4rem;
#     border: 1px solid #eee;
#     margin-bottom: 1rem;
# }}

# .mrag-answer-card {{
#     border-left: 4px solid {NAVY};
# }}

# .stButton > button {{
#     background: {CRIMSON};
#     color: white;
#     border: none;
#     border-radius: 8px;
#     font-weight: 600;
# }}

# .stButton > button:hover {{
#     background: {NAVY};
#     color: white;
# }}

# div[data-testid="stSidebar"] .stButton > button {{
#     background: #ffffff;
#     color: {NAVY};
#     border: 1px solid {NAVY};
#     text-align: left;
#     font-weight: 500;
#     font-size: 0.85rem;
#     white-space: normal;
# }}

# div[data-testid="stSidebar"] .stButton > button:hover {{
#     background: {NAVY};
#     color: white;
# }}

# div[data-testid="stExpander"] {{
#     border-left: 3px solid {CRIMSON};
#     border-radius: 8px;
# }}
# </style>
# """, unsafe_allow_html=True)

# # ---------------------------------------------------------
# # Header
# # ---------------------------------------------------------

# st.title("⚖️ मुलुकी RAG — Nepal Legal Assistant")
# st.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)

# st.markdown(
#     """
# Ask questions about Nepalese law using an **Agentic Hybrid RAG** system.

# The assistant retrieves relevant legal provisions and generates cited legal answers.
# """
# )

# st.caption("धर्मो रक्षति रक्षितः — कानूनी प्रश्नहरूको भरपर्दो उत्तर")

# # ---------------------------------------------------------
# # Session State
# # ---------------------------------------------------------

# if "question" not in st.session_state:
#     st.session_state.question = ""

# # ---------------------------------------------------------
# # Sidebar
# # ---------------------------------------------------------

# with st.sidebar:

#     st.markdown("### About")

#     st.caption(
#         "Muluki RAG retrieves relevant provisions from Nepal's Muluki "
#         "Criminal Code, Civil Code, and Domestic Violence Act."
#     )

#     st.markdown("---")

#     st.markdown("### Retrieval Strategy")

#     strategy = st.radio(
#         "Choose a strategy",
#         ["step_back", "original"],
#         index=0
#     )

#     if strategy == "step_back":
#         st.info(
#             "Best for complex legal questions. "
#             "The agent rewrites the query into a broader legal form."
#         )
#     else:
#         st.info(
#             "Uses your question exactly as written without rewriting."
#         )

#     st.markdown("---")

#     st.markdown("### Try an Example")

#     examples = [
#         "When can a prisoner be placed on parole?",
#         "What constitutes domestic violence under Nepali law?",
#         "What is the punishment for theft under the Muluki Criminal Code?",
#         "What are the grounds for divorce under the Civil Code?",
#     ]

#     for ex in examples:
#         if st.button(ex, key=ex, use_container_width=True):
#             st.session_state.question = ex
#             st.rerun()

# # ---------------------------------------------------------
# # User Input
# # ---------------------------------------------------------

# question = st.text_area(
#     "Enter your legal question",
#     value=st.session_state.question,
#     height=150,
#     placeholder="Example: When can a prisoner be placed on parole?"
# )

# ask = st.button(
#     "Ask Question",
#     type="primary",
#     use_container_width=True
# )

# # ---------------------------------------------------------
# # Query API
# # ---------------------------------------------------------

# if ask:

#     if question.strip() == "":
#         st.warning("Please enter a legal question.")
#         st.stop()

#     payload = {
#         "question": question,
#         "strategy": strategy
#     }

#     with st.spinner("Searching Nepalese law..."):

#         try:
#             response = requests.post(
#                 API_URL,
#                 json=payload,
#                 timeout=120
#             )

#             response.raise_for_status()
#             result = response.json()

#         except requests.exceptions.ConnectionError:
#             st.error(
#                 "Cannot connect to the FastAPI server.\n\n"
#                 "Start it using:\n"
#                 "`uvicorn api.main:app --reload`"
#             )
#             st.stop()

#         except Exception as e:
#             st.error(f"Error: {e}")
#             st.stop()

#     # -----------------------------------------------------
#     # Answer
#     # -----------------------------------------------------

#     st.markdown(
#         '<div class="mrag-card mrag-answer-card">',
#         unsafe_allow_html=True
#     )

#     st.markdown("#### 📖 Legal Answer")
#     st.write(result["answer"])

#     st.markdown("</div>", unsafe_allow_html=True)

#     # -----------------------------------------------------
#     # Sources
#     # -----------------------------------------------------

#     st.markdown("#### 📚 Cited Legal Sources")

#     sources = result.get("sources", [])

#     if len(sources) == 0:
#         st.info("No legal sources were returned.")

#     else:
#         for source in sources:

#             with st.expander(
#                 f"{source['citation']} • {source['source']} • Section {source['section_number']}"
#             ):

#                 st.markdown(
#                     f"**Section:** {source['section_number']}"
#                 )

#                 st.markdown(
#                     f"**Title:** {source['section_title']}"
#                 )

#                 st.markdown(
#                     f"**Source:** {source['source']}"
#                 )

#     # -----------------------------------------------------
#     # Citation Verification
#     # -----------------------------------------------------

#     st.markdown("#### ✅ Citation Verification")

#     citation = result.get("citation_check")

#     if citation is None:
#         st.warning("Citation verification was not performed.")

#     elif citation.get("valid", False):
#         st.success("All citations were successfully verified.")

#     else:
#         st.error("Some citations could not be verified.")

#         if "error" in citation:
#             st.caption(citation["error"])

# # ---------------------------------------------------------
# # Footer
# # ---------------------------------------------------------

# st.markdown("---")

# st.caption(
#     "मुलुकी RAG · Agentic Hybrid Retrieval · Nepal Civil & Criminal Law"
# )




import streamlit as st
from qa_pipeline import answer_question

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="मुलुकी RAG | Nepal Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

CRIMSON = "#DC143C"
NAVY = "#003893"

# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------

st.markdown(f"""
<style>
.accent-bar {{
    height: 4px;
    width: 130px;
    background: linear-gradient(90deg, {CRIMSON} 50%, {NAVY} 50%);
    border-radius: 2px;
    margin: 6px 0 22px 0;
}}

.mrag-card {{
    background: #ffffff;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    border: 1px solid #eee;
    margin-bottom: 1rem;
}}

.mrag-answer-card {{
    border-left: 4px solid {NAVY};
}}

.stButton > button {{
    background: {CRIMSON};
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}}

.stButton > button:hover {{
    background: {NAVY};
    color: white;
}}

div[data-testid="stSidebar"] .stButton > button {{
    background: #ffffff;
    color: {NAVY};
    border: 1px solid {NAVY};
    text-align: left;
    font-weight: 500;
    font-size: 0.85rem;
    white-space: normal;
}}

div[data-testid="stSidebar"] .stButton > button:hover {{
    background: {NAVY};
    color: white;
}}

div[data-testid="stExpander"] {{
    border-left: 3px solid {CRIMSON};
    border-radius: 8px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("⚖️ मुलुकी RAG — Nepal Legal Assistant")
st.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)

st.markdown(
    "Ask questions about Nepalese law — **Muluki Criminal Code, Civil Code, and the Domestic Violence Act** powered by Hybrid RAG."
)

st.caption("धर्मो रक्षति रक्षितः — कानूनी प्रश्नहरूको भरपर्दो उत्तर")

# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------

if "question" not in st.session_state:
    st.session_state.question = ""

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("### About")

    st.caption(
        "Muluki RAG retrieves relevant provisions from Nepal's Muluki Criminal Code, Civil Code, and Domestic Violence Act."
    )

    st.markdown("### Try an example")

    examples = [
        "When can a prisoner be placed on parole?",
        "What constitutes domestic violence under Nepali law?",
        "What is the punishment for theft under the Muluki Criminal Code?",
        "What are the grounds for divorce under the Civil Code?"
    ]

    for ex in examples:
        if st.button(ex, key=ex, use_container_width=True):
            st.session_state.question = ex
            st.rerun()

# ---------------------------------------------------------
# User Input
# ---------------------------------------------------------

question = st.text_area(
    "Enter your legal question",
    value=st.session_state.question,
    height=150,
    placeholder="Example: When can a prisoner be placed on parole?"
)

ask = st.button(
    "Ask Question",
    type="primary",
    use_container_width=True
)

# ---------------------------------------------------------
# Direct Backend Call
# ---------------------------------------------------------

if ask:

    if question.strip() == "":
        st.warning("Please enter a legal question.")
        st.stop()

    with st.spinner("Searching Nepalese law..."):

        try:
            # Direct call to qa_pipeline
            result = answer_question(question)

        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    # -----------------------------------------------------
    # Answer
    # -----------------------------------------------------

    st.markdown(
        '<div class="mrag-card mrag-answer-card">',
        unsafe_allow_html=True
    )

    st.markdown("#### 📖 Legal Answer")
    st.write(result["answer"])

    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # Sources
    # -----------------------------------------------------

    st.markdown("#### 📚 Cited Legal Sources")

    sources = result.get("sources", [])

    if not sources:
        st.info("No legal sources were returned.")

    else:
        for source in sources:

            with st.expander(
                f"{source['citation']} • {source['source']} • Section {source['section_number']}"
            ):

                st.markdown(f"**Section:** {source['section_number']}")
                st.markdown(f"**Title:** {source['section_title']}")
                st.markdown(f"**Source:** {source['source']}")

                if source.get("text"):
                    st.markdown("**Legal Text:**")
                    st.write(source["text"])

    # -----------------------------------------------------
    # Citation Verification
    # -----------------------------------------------------

    st.markdown("#### ✅ Citation Verification")

    citation = result.get("citation_check")

    if citation is None:
        st.warning("Citation verification was not performed.")

    elif citation.get("valid", False):
        st.success("All citations were successfully verified.")

    else:
        st.error("Some citations could not be verified.")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown("---")
st.caption("मुलुकी RAG · Muluki Criminal Code · Civil Code · Domestic Violence Act")