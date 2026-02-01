import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# -------- CONFIG --------
DATA_DIR = "D:\AdvancedML\chemical_rag_system\Documents"
VECTOR_DB_DIR = "vectorstore"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
# ------------------------

def load_documents():
    documents = []

    for topic in os.listdir(DATA_DIR):
        topic_path = os.path.join(DATA_DIR, topic)

        if not os.path.isdir(topic_path):
            continue

        for file in os.listdir(topic_path):
            if file.endswith(".pdf"):
                pdf_path = os.path.join(topic_path, file)
                loader = PyPDFLoader(pdf_path)
                pages = loader.load()

                for page in pages:
                    page.metadata["topic"] = topic
                    page.metadata["source"] = file

                documents.extend(pages)

    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_documents(documents)


def create_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTOR_DB_DIR)


if __name__ == "__main__":
    print("Loading documents...")
    docs = load_documents()
    print(f"Loaded {len(docs)} pages")

    print("Chunking documents...")
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks")

    print("Creating vector store...")
    create_vectorstore(chunks)

    print("✅ Ingestion complete. Vector store saved locally.")
