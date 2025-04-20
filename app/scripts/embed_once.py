from app.services.embedding_loader import load_and_chunk
from app.services.vector_store import store_chunks_in_vector_db
# export PYTHONPATH=$(pwd)
# python app/scripts/embed_once.py

file_path = "data/englisch_aufenthg.pdf" # this should be dynamic though

chunks = load_and_chunk(file_path) 
store_chunks_in_vector_db(chunks)

print("embedding completed")