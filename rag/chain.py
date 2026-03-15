"""
RAG chain — combines retriever + Groq (Llama 3.3 70B) for grounded Q&A.
Uses modern LangChain LCEL (compatible with langchain >= 0.3).
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, AIMessage


SYSTEM_TEMPLATE = """You are an expert energy data analyst assistant.
Your role is to analyze operational energy data and provide clear, actionable insights.

Use ONLY the context provided below to answer the question.
If the answer is not in the context, say: "I don't have enough data to answer this question."

Always:
- Be precise and quantitative when data is available
- Highlight anomalies, trends, or notable patterns
- Suggest potential causes or actions when relevant
- Format numbers clearly (with units and decimals)

Context:
{context}
"""

PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_TEMPLATE),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(retriever, api_key: str):
    """Build a modern LCEL RAG chain with Groq Llama 3.3 70B."""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=api_key,
        temperature=0.2,
    )

    chain = (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(retriever.invoke(x["question"])),
        )
        | PROMPT
        | llm
        | StrOutputParser()
    )

    return chain


def run_chain(chain, retriever, question: str, chat_history: list) -> dict:
    """
    Run the chain and return answer + source documents.
    chat_history: list of {"role": "user"/"assistant", "content": str}
    """
    messages = []
    for msg in chat_history[:-1]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    source_docs = retriever.invoke(question)

    answer = chain.invoke({
        "question": question,
        "chat_history": messages,
    })

    return {
        "answer": answer,
        "source_documents": source_docs,
    }
