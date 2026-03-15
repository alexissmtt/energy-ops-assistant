"""
Utility helpers — file saving, formatting, session management.
"""

import os
import tempfile
import hashlib
from pathlib import Path


def save_uploaded_file(uploaded_file) -> str:
    """Save a Streamlit UploadedFile to a temp path and return the path."""
    suffix = Path(uploaded_file.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name


def file_hash(file_path: str) -> str:
    """Return MD5 hash of file — used to detect if same file re-uploaded."""
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def format_sources(source_docs: list) -> str:
    """Format source documents into a readable string for display."""
    seen = set()
    lines = []
    for doc in source_docs:
        src = doc.metadata.get("source", "Unknown")
        doc_type = doc.metadata.get("type", "")
        key = f"{src}_{doc_type}"
        if key not in seen:
            seen.add(key)
            if doc_type == "summary":
                lines.append(f"📊 **{src}** — statistical summary")
            elif doc_type == "rows":
                r_start = doc.metadata.get("row_start", "?")
                r_end = doc.metadata.get("row_end", "?")
                lines.append(f"📋 **{src}** — rows {r_start}–{r_end}")
            else:
                page = doc.metadata.get("page", "?")
                lines.append(f"📄 **{src}** — page {page}")
    return "\n".join(lines) if lines else "No sources found."


EXAMPLE_QUESTIONS = [
    "What is the average energy consumption across all sites?",
    "Which site has the highest peak demand? When did it occur?",
    "Are there any anomalies or unusual patterns in the data?",
    "What is the trend in renewable energy production over time?",
    "Compare consumption between the top 3 highest-consuming sites.",
    "What percentage of total energy comes from renewable sources?",
]
