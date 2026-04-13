import requests
import streamlit as st

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="RAG Assistant", page_icon="🤖", layout="wide")
st.title("🤖 RAG-based AI Assistant")

with st.sidebar:
    st.header("Ingestion")
    uploaded_files = st.file_uploader(
        "Upload documents (PDF/TXT/MD/DOCX)",
        accept_multiple_files=True,
        type=["pdf", "txt", "md", "docx"],
    )

    if st.button("Index Documents", type="primary"):
        if not uploaded_files:
            st.warning("Please upload at least one document.")
        else:
            files_payload = [
                ("files", (f.name, f.getvalue(), f"application/{f.type}")) for f in uploaded_files
            ]
            response = requests.post(f"{BACKEND_URL}/api/v1/ingest", files=files_payload, timeout=300)
            if response.ok:
                st.success("Documents indexed successfully.")
                st.json(response.json())
            else:
                st.error(f"Ingestion failed: {response.text}")

st.subheader("Ask Questions")
question = st.text_area("Question", placeholder="Ask anything from uploaded documents...")

if st.button("Ask", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        payload = {"question": question}
        response = requests.post(f"{BACKEND_URL}/api/v1/query", json=payload, timeout=180)

        if response.ok:
            result = response.json()
            st.markdown("### Answer")
            st.write(result["answer"])

            st.markdown("### Sources")
            for idx, src in enumerate(result.get("sources", []), start=1):
                with st.expander(f"Source {idx}"):
                    st.write(src.get("content", ""))
                    st.json(src.get("metadata", {}))
        else:
            st.error(f"Query failed: {response.text}")
