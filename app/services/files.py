import os, shutil
from uuid import uuid4
from sqlalchemy.orm import Session
from app.services.embedding_loader import load_and_chunk
from app.services.vector_store import store_chunks_in_vector_db
from app.db.models import UserFile
from fastapi import HTTPException

async def handle_file_upload(file, user_id: int, db: Session) -> str: 
    file_key = f"{user_id}_{uuid4().hex}" # formatting a string and generates a randomly generated Universally Unique Identifier (UUID)
    # the hex is for a plain hexadecimal string — without any dashes
    file_path = f"data/user_{user_id}/{file_key}_{file.filename}" # this we dont't need cause it is direct

    os.makedirs(os.path.dirname(file_path), exist_ok=True) # os.makedirs() to suppress errors if the directory already exists.
    with open(file_path, "wb") as buffer: 
        # with Ensures the file is properly closed after the block finishes (even if errors happen).
        # wb stands for write binary
        # buffer becomes the file object you can write to.  
        shutil.copyfileobj(file.file, buffer)
        # Read from file.file, and write everything into buffer.

        # so we make a buffer first to write the binary in and then if all goes well, we save it

        # then now the file path should be ready to extract context from

    chunks = load_and_chunk(file_path) 
    vector_path = f"db/faiss_user_{user_id}_{file_key}"
    store_chunks_in_vector_db(chunks, persist_dir=vector_path)

    db_file = UserFile(
        user_id=user_id,
        file_key=file_key, # what we did was for this one
        filename=file.filename,
        file_path=file_path # and this one
    )
    db.add(db_file)
    db.commit()
    return file_key

async def delete_user_file(file_key: str, user_id: int, db: Session):
    file = db.query(UserFile).filter_by(file_key=file_key, user_id=user_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Delete physical file
    if os.path.exists(file.file_path):
        os.remove(file.file_path)

    # Delete FAISS vector store
    vector_path = f"db/faiss_user_{user_id}_{file_key}"
    if os.path.exists(vector_path):
        shutil.rmtree(vector_path)

    # Delete DB record
    db.delete(file)
    db.commit()
    return {"message": "File and associated vector store deleted successfully"}

# except for saving the files, handling the files is what we have already learned in OS
    