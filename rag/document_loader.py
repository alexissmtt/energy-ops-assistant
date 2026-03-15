"""
Document loader module — handles PDF and CSV ingestion.
"""

import pandas as pd
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf(file_path: str) -> list[Document]:
    """Load and split a PDF into LangChain Documents."""
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " "],
    )
    return splitter.split_documents(pages)


def load_csv(file_path: str) -> list[Document]:
    """
    Load a CSV and convert each row + aggregated stats into Documents.
    Produces two types of chunks:
      1. Row-level chunks (batched for efficiency)
      2. A statistical summary chunk
    """
    df = pd.read_csv(file_path)
    documents = []

    # --- Statistical summary ---
    summary_lines = [f"Dataset: {Path(file_path).name}",
                     f"Rows: {len(df)} | Columns: {list(df.columns)}"]
    for col in df.select_dtypes(include="number").columns:
        stats = df[col].describe()
        summary_lines.append(
            f"{col} → mean={stats['mean']:.2f}, min={stats['min']:.2f}, "
            f"max={stats['max']:.2f}, std={stats['std']:.2f}"
        )
    documents.append(Document(
        page_content="\n".join(summary_lines),
        metadata={"source": Path(file_path).name, "type": "summary"},
    ))

    # --- Row-level chunks (batch of 30 rows each) ---
    batch_size = 30
    for i in range(0, len(df), batch_size):
        chunk = df.iloc[i: i + batch_size]
        content = f"Rows {i}–{i + len(chunk) - 1}:\n{chunk.to_string(index=False)}"
        documents.append(Document(
            page_content=content,
            metadata={"source": Path(file_path).name, "type": "rows",
                      "row_start": i, "row_end": i + len(chunk) - 1},
        ))

    return documents


def load_file(file_path: str) -> list[Document]:
    """Dispatch loader based on file extension."""
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".csv":
        return load_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Please upload a PDF or CSV.")
