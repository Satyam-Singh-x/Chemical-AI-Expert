🧪 Chemical Expert – Domain-Specific RAG System for Chemical Engineering

A Retrieval-Augmented Generation (RAG) based Chemical Engineering Knowledge Assistant designed for academic, professional, and reference use.

This system combines domain-specific chemical engineering documents, vector search (FAISS), local LLM inference via Ollama, LangChain, LangGraph memory, and a Streamlit UI to deliver accurate, safe, and citation-grounded answers.

🚀 Key Highlights

🔍 Domain-specific RAG (Chemical Engineering only)

📚 Supports Reaction Engineering, Unit Operations, Process Safety, MSDS, Equipment Basics

🧠 Local LLM inference using Ollama (Qwen 2.5)

🗂 FAISS vector store for fast semantic retrieval

🧩 LangGraph memory with thread-based conversation tracking

🧪 Strict anti-hallucination & safety-first system prompt

📊 Clean Streamlit Chat UI

🔒 No cloud dependency for inference (fully local)

📐 System Architecture


User Query

   ↓
LangGraph State (Thread-based Memory)

   ↓
RAG Chain

   ├── Retriever (FAISS Vector Store)
   
   ├── Context Formatter
   
   ├── System Prompt
   
   └── Local LLM (Ollama)
   ↓
Final Answer (Context-grounded)


📁 Project Structure

chemical_rag_system/

│
├── app.py

├── chatbot_backend.py

├── rag_chain.py

├── prompts.py

├── ingest.py

├── vectorstore/

│   ├── index.faiss

│   └── index.pkl

├── data/

│   └── pdfs/

├── requirements.txt

└── README.md

🧠 File-by-File Explanation



🔹 app.py

Streamlit frontend

Provides a ChatGPT-style UI

Manages user sessions and thread IDs

Streams responses token-by-token

Displays conversation history cleanly

Key responsibilities

UI rendering

Message streaming

Thread management



🔹 chatbot_backend.py

LangGraph orchestration layer

Defines the conversation state

Manages memory using thread IDs

Connects Streamlit input → RAG chain → response

Ensures only the latest user query is passed to the retriever

Key responsibilities

State management

Conversation memory

Safe RAG invocation



🔹 rag_chain.py

Core RAG pipeline

Loads FAISS vector store

Initializes local Ollama LLM

Builds the RAG chain using LangChain Runnables

Ensures retriever receives string input only

Formats retrieved documents into context

Key components

load_retriever()

load_llm()

build_rag_chain()



🔹 prompts.py

System prompt configuration

Enforces:

No hallucination

Context-only answers

Safety-first responses

Controls tone, explanation style, and formatting

Forces undergraduate-level clarity with professional rigor

This file defines the behavioral intelligence of the assistant.



🔹 ingest.py

Document ingestion & indexing

Loads PDFs from data/pdfs/

Cleans and chunks text

Attaches metadata (source, topic, page)

Embeds content using sentence-transformers

Saves FAISS index locally

Run once unless documents change.


🔹 vectorstore/

Persistent FAISS index

Stores embedded document chunks

Enables fast semantic search

Can be committed to GitHub for deployment



🔹 data/pdfs/

Knowledge source directory

Contains authoritative Chemical Engineering material such as:

Reaction Engineering textbooks

Unit Operations manuals

MSDS / SDS documents

Process safety handbooks

Equipment fundamentals

⬇️ Clone / Pull Instructions (IMPORTANT)

🔹 Clone the repository (first-time users)

git clone https://github.com/Satyam-Singh-x/Chemical-AI-Expert.git

cd chemical_rag_system

🔹 Pull latest updates (existing users)

If you already have the repository:

git pull origin master


(or main, depending on your default branch)

🔹 If vectorstore is updated by the author

Always pull before running the app to ensure the latest embeddings are available:

git pull


No re-ingestion is required if vectorstore/ is already present.

⚙️ Installation & Setup

1️⃣ Create virtual environment (Python 3.10 recommended)

python -m venv .venv

.venv\Scripts\activate

2️⃣ Install dependencies

pip install -r requirements.txt


Key libraries

langchain

langchain-community

langchain-ollama

langgraph

faiss-cpu

sentence-transformers

streamlit

3️⃣ Start Ollama

ollama serve

ollama pull qwen2.5

4️⃣ Ingest documents (one-time)

python ingest.py


Skip this step if vectorstore/ is already present.

5️⃣ Run the application

streamlit run app.py

🛡 Safety & Accuracy Principles

❌ No hallucinated content

❌ No external knowledge beyond documents

❌ No unsafe procedural instructions

✅ Context-grounded explanations only

✅ Engineering intuition before equations

✅ Clear refusal when data is missing

📌 Example Capabilities

✔ Explain reactor design concepts

✔ Clarify transport phenomena intuitively

✔ Summarize unit operation principles

✔ Interpret MSDS information safely

✔ Provide citation-aware explanations

🎯 Intended Use Cases

Chemical engineering students

Exam preparation

Interview preparation

Research reference

Knowledge validation

Educational demos of RAG systems

🔮 Future Enhancements

📌 Explicit citation display

📊 Retrieval confidence scoring

🧠 Topic-based metadata filtering

🔄 Document re-ingestion UI

📎 PDF page-level linking

📜 License

This project is intended for educational and research purposes only.

👤 Author

Satyam
Chemical Engineering + AI
Jadavpur University
