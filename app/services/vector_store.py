from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import os

def store_chunks_in_vector_db(chunks: list[Document], persist_dir="db/chroma_store"):
    embedding_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_dir
    )
    
    vector_db.persist()
    return vector_db

def load_vector_db(persist_dir="db/chroma_store"):
    embedding_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    return Chroma(persist_directory=persist_dir, embedding_function=embedding_model)

def retrieve_relevant_chunks(query: str, k=3) -> list[str]:
    db = load_vector_db()
    results = db.similarity_search(query, k=k)
    return [doc.page_content for doc in results]