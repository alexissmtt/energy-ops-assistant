<div align="center">

# ⚡ Energy Ops Assistant

> A GenAI-powered tool for operational energy data analysis — ask questions about your energy reports and sensor data in plain English.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://energy-ops-assistant.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-green)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-F55036)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

</div>

---

## 🎯 Overview

**Energy Ops Assistant** is a Retrieval-Augmented Generation (RAG) application that allows operations teams to interact with energy data — CSV sensor logs, SCADA exports, or PDF maintenance reports — using natural language.

Instead of writing SQL queries or digging through spreadsheets, an operator can simply ask:
- *"Which site had the highest CO₂ emissions last quarter?"*
- *"Are there any anomalies in Site B's consumption data?"*
- *"What is the trend in renewable energy production?"*

The assistant retrieves the relevant data chunks and generates a grounded, accurate answer using **Llama 3.3 70B**.

---

## 🚀 Live Demo

👉 **[Try it here](https://energy-ops-assistant.streamlit.app)**

1. Enter your free [Groq API key](https://console.groq.com) in the sidebar
2. Upload a CSV or PDF file — or click **Load Sample Energy Data**
3. Ask questions in plain English

---

## 🏗️ Architecture
```
User Query
    │
    ▼
Streamlit UI (app.py)
    │
    ├── Document Loader (rag/document_loader.py)
    │       PDF → PyPDFLoader + text splitter
    │       CSV → pandas → row batches + statistical summary
    │
    ├── Embedding + Indexing (rag/vector_store.py)
    │       HuggingFace all-MiniLM-L6-v2 → FAISS index
    │
    └── RAG Chain (rag/chain.py)
            Retriever (top-k similarity) → Llama 3.3 70B → Answer
```

**Stack:**
| Component | Technology |
|---|---|
| LLM | Groq Llama 3.3 70B |
| Embeddings | HuggingFace all-MiniLM-L6-v2 (local) |
| Vector Store | FAISS (in-memory) |
| Orchestration | LangChain |
| UI | Streamlit |
| Data | Pandas |

---

## 📊 Sample Data

The project includes a synthetic energy dataset (`data/sample/sample_energy_data.csv`) with:
- **1,825 records** across **5 sites** (Hong Kong, Shenzhen, Shanghai, Beijing, Guangzhou)
- **365 days** of daily readings per site (2024)
- Features: consumption, solar/wind production, grid import, CO₂ emissions, peak demand
- Realistic seasonal patterns and injected anomalies (~2%)

---

## 💬 Example Questions

Once a file is loaded, try asking:
- *"What is the average daily consumption per site?"*
- *"Which day had the highest peak demand and where?"*
- *"What percentage of energy comes from renewables?"*
- *"Are there any anomalies? When and where did they occur?"*
- *"Compare CO₂ emissions between Site A and Site B."*

---

## 📁 Project Structure
```
energy-ops-assistant/
├── app.py                        # Streamlit application
├── rag/
│   ├── document_loader.py        # PDF & CSV ingestion + chunking
│   ├── vector_store.py           # FAISS index + local HuggingFace embeddings
│   └── chain.py                  # Conversational RAG chain (Groq)
├── utils/
│   └── helpers.py                # File utils, source formatting
├── data/
│   └── sample/
│       ├── generate_sample.py    # Sample data generator
│       └── sample_energy_data.csv
├── .env.example                  # API key template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔒 Security Notes

- Your Groq API key is entered via the sidebar and never stored to disk
- All document processing and embeddings run locally — only the final LLM call is sent to Groq

---

## 🌍 Real-World Applications

This project mirrors tools used in industrial operations (e.g., water treatment, waste management, energy infrastructure) where operators need to quickly extract insights from large volumes of sensor and report data — a core use case at companies like **Veolia**, **Engie**, or **EDF**.

---

## 📄 License

MIT

---

<div align="center">
Made by <a href="https://github.com/alexissmtt">Alexis Mattei</a>
</div>
