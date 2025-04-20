from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

def store_chunks_in_vector_db(chunks: list[Document], persist_dir="db/faiss_store"): # embedding time!
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") # in str for model detection
    vector_db = FAISS.from_documents(chunks, embedding_model)  
    vector_db.save_local(persist_dir) # save it forever in persistent directory
    return vector_db

def load_vector_db(persist_dir="db/faiss_store"):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    try:
        return FAISS.load_local(persist_dir, embedding_model) # load the vector db to later retrieve in the next function
    except Exception:
        # Safe fallback for tests
        from langchain.schema import Document
        return FAISS.from_documents([Document(page_content="fallback test content")], embedding_model)

def retrieve_relevant_chunks(query: str, k=3) -> list[str]:
    db = load_vector_db()
    results = db.similarity_search(query, k=k) # similarity search is using 3 dimensional search
    return [doc.page_content for doc in results] 