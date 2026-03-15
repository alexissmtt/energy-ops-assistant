"""
Vector store module — builds and queries a FAISS index with local HuggingFace embeddings.
Uses sentence-transformers locally (no API quota, works offline).
"""

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document


def build_vector_store(documents: list[Document], api_key: str = None) -> FAISS:
    """Embed documents and build a FAISS index using local embeddings."""
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store


def get_retriever(vector_store: FAISS, k: int = 5):
    """Return a similarity-search retriever."""
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
