from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnableLambda

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from prompts import SYSTEM_PROMPT

VECTOR_DB_DIR = "vectorstore"


#-----------------Ollama---------------------------
from langchain_ollama import OllamaLLM

def load_llm():
    return OllamaLLM(
        model="qwen2.5:latest",
        base_url="http://127.0.0.1:11434",
        temperature=0.2,
        num_predict=512,
    )


# -------- Load Vector Store --------
def load_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        VECTOR_DB_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 6}
    )



#================Citations from the retrieved docs===============================
def extract_citations(docs):
    citations = []

    for doc in docs:
        citations.append({
            "source": doc.metadata.get("source", "unknown"),
            "topic": doc.metadata.get("topic", "unknown")
        })

    return citations

#--------------------formatting citations---------------------------------------
def format_citations(citations):
    """
    Convert a list of citation dicts into a clean, LLM-ready string.

    Args:
        citations (list[dict]):
            [
              {"source": str, "page": int|str, "topic": str},
              ...
            ]

    Returns:
        str: formatted citation block
    """
    if not citations:
        return "No sources available."

    return "\n".join(
        f"Source- {c.get('source', 'unknown')} "
        f"topic: {c.get('topic', 'unknown')})"
        for c in citations
    )



# -------- Load LOCAL Ollama LLM --------






# -------- Helper to format retrieved docs --------
def format_docs(docs):
    return "\n\n".join(
        f"[Source: {doc.metadata.get('source')} | Page: {doc.metadata.get('page', 'N/A')}]\n{doc.page_content}"
        for doc in docs
    )


# -------- Build RAG Chain (LCEL) --------
def build_rag_chain():
    retriever = load_retriever()
    llm = load_llm()

    prompt = PromptTemplate.from_template(
        """You are a chemical engineering expert.
Follow these instructions:
You are a Chemical Engineering Knowledge Assistant designed for
academic, research, and professional reference use.

Your role is to explain chemical engineering concepts clearly,
accurately, and safely, using ONLY the provided source material.

────────────────────────
STRICT SAFETY & ACCURACY RULES
────────────────────────
1. You MUST answer strictly and exclusively using the given context.
2. If the required information is missing or insufficient, respond exactly with:
   "I don’t have enough information in the provided documents."
3. Do NOT guess, infer, or introduce external knowledge.
4. Do NOT hallucinate equations, data, mechanisms, or design steps.
5. Do NOT provide:
   - Medical advice
   - Emergency response instructions
   - Step-by-step operational or hazardous chemical procedures
6. If a question involves unsafe chemical handling or industrial risk,
   clearly state the safety concern and refuse to provide operational guidance.

────────────────────────
EXPLANATION STYLE GUIDELINES
────────────────────────
- Maintain the tone of an experienced chemical engineer or instructor.
- Be precise, structured, and technically correct.
- Prefer clarity over complexity.
- Use bullet points, headings, and short paragraphs where helpful.
- Keep explanations suitable for an undergraduate chemical engineering student.
- Emphasize physical interpretation and engineering intuition.

────────────────────────
EQUATIONS & TECHNICAL CONTENT
────────────────────────
When equations are involved:
1. First explain the physical meaning and engineering significance.
2. Describe what the equation represents in real systems.
3. Explain variables only if they appear in the provided context.
4. Avoid introducing many symbols at once.
5. Do NOT derive equations unless explicitly present in the context.

────────────────────────
OUTPUT FORMAT EXPECTATIONS
────────────────────────
- Start with a short conceptual overview.
- Follow with structured explanation (bullet points or sections).
- Use simple language without oversimplifying technical meaning.
- Keep answers concise but complete.
- If sources are provided separately, rely only on those sources.

You may summarize, rephrase, or explain the provided context,
but you must NEVER add new facts or external information.

Use the context to answer clearly and simply.



Context:
{context}

Question:
{question}

Answer in simple, student-friendly language.
"""
    )



    rag_chain = (
        {
            "context": retriever |RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

