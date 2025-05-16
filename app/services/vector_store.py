import numpy as np
from sklearn.preprocessing import normalize
import faiss
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores.utils import DistanceStrategy
from pathlib import Path


def store_chunks_in_vector_db(chunks: list[Document], persist_dir="db/faiss_store"):
    if not chunks:
        raise ValueError("No chunks provided to store in vector database.")

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = FAISS.from_documents(chunks, embedding_model)

    Path(persist_dir).mkdir(parents=True, exist_ok=True)
    vector_db.save_local(str(persist_dir))

    return vector_db
def load_vector_db(persist_dir="db/faiss_store"):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(persist_dir, embedding_model, allow_dangerous_deserialization=True)

def retrieve_relevant_chunks(query: str, k=3) -> list[str]:
    db = load_vector_db()
    results = db.similarity_search(query, k=k) # similarity search is using 3 dimensional search
    return [doc.page_content for doc in results]
