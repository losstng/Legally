from app.services.vector_store import load_vector_db, retrieve_relevant_chunks

def get_context_from_file(file_key: str, user_id: int, question: str) -> str: # essentially retrieving from the vector db
    vector_path = f"db/faiss_user_{user_id}_{file_key}"
    db = load_vector_db(vector_path)
    results = db.similarity_search(question, k=5) # top 5 results
    return "\n\n".join([doc.page_content for doc in results]) # doc is defined through the process, join together from chunks for coherent

def get_context_from_global(question: str, max_tokens=1500) -> str: 
    return retrieve_relevant_chunks(question, k=10)  # Already token-limited