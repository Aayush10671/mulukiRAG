import streamlit as st
import requests

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Nepal Legal RAG",
    page_icon="⚖️",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/query"

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("⚖️ Nepal Legal RAG Assistant")
st.markdown(
    """
    Ask questions about **Nepalese law** using a **Hybrid Retrieval-Augmented Generation (RAG)** system.

    The system retrieves the most relevant legal provisions and generates a cited legal answer.
    """
)

# ---------------------------------------------------------
# User Input
# ---------------------------------------------------------

question = st.text_area(
    "Enter your legal question",
    height=150,
    placeholder="Example: When can a prisoner be placed on parole?"
)

# ---------------------------------------------------------
# Ask Button
# ---------------------------------------------------------

if st.button("Ask Question", type="primary", use_container_width=True):

    if question.strip() == "":
        st.warning("Please enter a legal question.")
        st.stop()

    payload = {
        "question": question
    }

    with st.spinner("Searching Nepalese law..."):

        try:
            response = requests.post(
                API_URL,
                json=payload,
                timeout=120
            )

            response.raise_for_status()
            result = response.json()

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the FastAPI server.\n\n"
                "Start it using:\n"
                "`uvicorn api.main:app --reload`"
            )
            st.stop()

        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    # -----------------------------------------------------
    # Answer
    # -----------------------------------------------------

    st.markdown("## 📖 Legal Answer")
    st.write(result["answer"])

    # -----------------------------------------------------
    # Sources
    # -----------------------------------------------------

    st.markdown("## 📚 Cited Legal Sources")

    sources = result.get("sources", [])

    if len(sources) == 0:
        st.info("No legal sources were returned.")

    else:
        for source in sources:

            with st.expander(
                f"{source['citation']} • {source['source']} • Section {source['section_number']}"
            ):

                st.markdown(
                    f"**Section:** {source['section_number']}"
                )

                st.markdown(
                    f"**Title:** {source['section_title']}"
                )

                st.markdown(
                    f"**Source:** {source['source']}"
                )

    # -----------------------------------------------------
    # Citation Verification
    # -----------------------------------------------------

    st.markdown("## ✅ Citation Verification")

    citation = result.get("citation_check")

    if citation is None:
        st.warning("Citation verification was not performed.")

    elif citation.get("valid", False):
        st.success("All citations were successfully verified.")

    else:
        st.error("Some citations could not be verified.")

        if "error" in citation:
            st.caption(citation["error"])