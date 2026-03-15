"""
Energy Ops Assistant — Streamlit application entry point.
A RAG-powered GenAI tool for operational energy data analysis.
"""

import os
import streamlit as st
from pathlib import Path

from rag.document_loader import load_file
from rag.vector_store import build_vector_store, get_retriever
from rag.chain import build_rag_chain, run_chain
from utils.helpers import save_uploaded_file, file_hash, format_sources, EXAMPLE_QUESTIONS

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Energy Ops Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a73e8;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #5f6368;
        margin-bottom: 1.5rem;
    }
    .stChatMessage { border-radius: 12px; }
    .source-box {
        background: #f8f9fa;
        border-left: 3px solid #1a73e8;
        padding: 0.6rem 1rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.82rem;
        color: #5f6368;
        margin-top: 0.4rem;
    }
    .badge {
        display: inline-block;
        background: #e8f0fe;
        color: #1a73e8;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 4px;
    }
    .example-btn { cursor: pointer; }
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key, default in {
    "messages": [],
    "chain": None,
    "retriever": None,
    "current_file_hash": None,
    "file_name": None,
    "doc_count": 0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ Energy Ops Assistant")
    st.markdown("*Powered by Llama 3.3 70B + RAG*")
    st.divider()

    # API Key input
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your free key at console.groq.com",
    )

    st.divider()

    # File upload
    st.markdown("### 📂 Upload Data")
    uploaded_file = st.file_uploader(
        "Upload a CSV or PDF file",
        type=["csv", "pdf"],
        help="Energy reports, sensor logs, operational data…",
    )

    # Load sample data button
    st.markdown("**Or use sample data:**")
    use_sample = st.button("⚡ Load Sample Energy Data", use_container_width=True)

    st.divider()

    # Stats panel
    if st.session_state.file_name:
        st.markdown("### 📊 Loaded Document")
        st.markdown(f"**File:** `{st.session_state.file_name}`")
        st.markdown(f"**Chunks indexed:** `{st.session_state.doc_count}`")
        st.markdown('<span class="badge">✓ Ready</span>', unsafe_allow_html=True)

    st.divider()
    st.markdown(
        "<small>Built with LangChain · FAISS · Llama 3.3 70B<br>"
        "© 2025 energy-ops-assistant</small>",
        unsafe_allow_html=True,
    )


# ── Helper: build chain from file ────────────────────────────────────────────
def build_chain_from_path(file_path: str, file_name: str, api_key: str):
    with st.spinner(f"🔍 Indexing **{file_name}**…"):
        docs = load_file(file_path)
        vs = build_vector_store(docs, api_key)
        retriever = get_retriever(vs)
        chain = build_rag_chain(retriever, api_key)
        st.session_state.chain = chain
        st.session_state.retriever = retriever
        st.session_state.file_name = file_name
        st.session_state.doc_count = len(docs)
        st.session_state.messages = []
    st.success(f"✅ **{file_name}** indexed — {len(docs)} chunks ready.")


# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">⚡ Energy Ops Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Ask questions about your energy data in natural language — '
    'powered by Llama 3.3 70B & Retrieval-Augmented Generation.</div>',
    unsafe_allow_html=True,
)

# Validate API key
if not api_key:
    st.info("👈 Enter your **Groq API Key** in the sidebar to get started.")
    st.stop()

# Handle file upload
if uploaded_file:
    fh = file_hash.__wrapped__(uploaded_file) if hasattr(file_hash, "__wrapped__") else None
    # Simple check: re-index only if new file
    if uploaded_file.name != st.session_state.file_name:
        tmp_path = save_uploaded_file(uploaded_file)
        build_chain_from_path(tmp_path, uploaded_file.name, api_key)

# Handle sample data
SAMPLE_PATH = Path(__file__).parent / "data" / "sample" / "sample_energy_data.csv"
if use_sample:
    if "sample_energy_data.csv" != st.session_state.file_name:
        build_chain_from_path(str(SAMPLE_PATH), "sample_energy_data.csv", api_key)

# No file loaded yet
if not st.session_state.chain:
    st.markdown("### 🚀 Get Started")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**What you can do:**
- 📊 Analyze energy consumption trends
- 🔍 Detect anomalies and outliers
- ⚖️ Compare sites or time periods
- 🌿 Assess renewable energy share
- 📈 Identify peak demand patterns
        """)
    with col2:
        st.markdown("""
**Supported formats:**
- **CSV** — sensor logs, SCADA exports, meter readings
- **PDF** — maintenance reports, audit documents, dashboards

**Example questions:**
        """)
        for q in EXAMPLE_QUESTIONS[:3]:
            st.markdown(f"- *{q}*")
    st.stop()

# ── Chat interface ────────────────────────────────────────────────────────────
st.markdown(f"### 💬 Chat — `{st.session_state.file_name}`")

# Example questions row
st.markdown("**Quick questions:**")
cols = st.columns(3)
for i, q in enumerate(EXAMPLE_QUESTIONS):
    if cols[i % 3].button(q, key=f"eq_{i}", use_container_width=True):
        st.session_state.pending_question = q

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📎 Sources used", expanded=False):
                st.markdown(
                    f'<div class="source-box">{msg["sources"]}</div>',
                    unsafe_allow_html=True,
                )

# Handle pending question from quick buttons
if "pending_question" in st.session_state:
    prompt = st.session_state.pop("pending_question")
else:
    prompt = st.chat_input("Ask anything about your energy data…")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data…"):
            result = run_chain(
                st.session_state.chain,
                st.session_state.retriever,
                prompt,
                st.session_state.messages,
            )
            answer = result.get("answer", "I could not generate an answer.")
            sources = format_sources(result.get("source_documents", []))

        st.markdown(answer)
        with st.expander("📎 Sources used", expanded=False):
            st.markdown(
                f'<div class="source-box">{sources}</div>',
                unsafe_allow_html=True,
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })

# Clear chat button
if st.session_state.messages:
    if st.button("🗑️ Clear conversation", key="clear"):
        st.session_state.messages = []
        # Rebuild chain to reset memory
        if st.session_state.file_name:
            file_path = (
                str(SAMPLE_PATH)
                if st.session_state.file_name == "sample_energy_data.csv"
                else None
            )
            if file_path:
                docs = load_file(file_path)
                vs = build_vector_store(docs, api_key)
                retriever = get_retriever(vs)
                st.session_state.chain = build_rag_chain(retriever, api_key)
                st.session_state.retriever = retriever
        st.rerun()
