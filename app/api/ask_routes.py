from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import uuid4
from app.db.database import get_db
from app.db import models
from app.db.models import UserFile
from app.schemas.ask import ApiResponse, HistoryResponseItem
from app.utils.security import get_current_user
from datetime import datetime
from app.utils.redis import redis_client
from app.services.llm import ask_legal_question_with_context, get_limited_context
from app.services.vector_store import retrieve_relevant_chunks, store_chunks_in_vector_db
from app.services.embedding_loader import load_and_chunk
from app.services.agents import process_legal_question
from app.utils.language import detect_language, SUPPORTED_LANGUAGES
from app.services.files import handle_file_upload, delete_user_file
from app.services.context import get_context_from_file, get_context_from_global
from app.services.ask import generate_full_answer
import shutil
import os
# wow, the whole trinity is here, crazy right? 


router = APIRouter() # an extension of taking different routes for the api, rather than calling the app directly
# relieving the main.py of the pain of being overstocked

@router.post("/ask", response_model=ApiResponse) # how should the function respond
# also routed throught the @router
async def ask_question( # async function, where. it is single threaded but efficient 
    question: str = Form(...), 
    file: UploadFile = File(None), # default value is none, opened for file upload
    file_key: str = Form(None), # same default value, but it is aform for string
    chat_session_id: int =Form(None),
    db: Session = Depends(get_db), # getting the session
    current_user: models.User = Depends(get_current_user) #authentication and stuff
):
    cached_answer = redis_client.get(f"qa:{question}") # try if any similar questioned has been asked
    if cached_answer: # if "yes" then return the data and the message of Boolean True
        return ApiResponse(success=True, data=
                           {"question": question, #the keys have to be exact
                           "answer": cached_answer}) # the data is then stored under json, or dictionary
    

    if file: # if a file is uploaded
        file_key = handle_file_upload(file, current_user.id, db) # upload it and assign a file key
        context = get_context_from_file(file_key, current_user.id, question) # get context from the file
    elif file_key: # if given a file key, which has been uploaded before
        context = get_context_from_file(file_key, current_user.id, question) # the same from file
    else:
        context = get_context_from_global(question) # note that it is "from_global"

    base, full, _ = generate_full_answer(question, context)

# def generate_full_answer(question: str, context: str) -> tuple[str, str, str]:
#   lang = detect_language(question)
#   base = ask_legal_question_with_context(question, context, lang)
#   full = process_legal_question(question, context, base, lang)
#   return base, full, lang ### note this or that it is being returned in
    redis_client.setex(f"qa:{question}", 3600, full) # caching the response for storage efficiency
    # setex = set expiry
    # what will be the key, what is the length for epxiration, and what is the data in it
    convo = models.Conversation(user_id=current_user.id, chat_session_id=chat_session_id, question=question, base_answer=base, full_answer=full)
    # saving to database, but still it begs the question of multiple Q&A in one convo, could be inefficient
    db.add(convo) 
    db.commit()
    db.refresh(convo)

    return ApiResponse(success=True, data={
        "question": convo.question,
        "answer": convo.full_answer
    }) # loading the simple stuff to response for the frontend, standardized for better coordination

@router.get("/files")
async def list_user_files(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    files = db.query(models.UserFile).filter(models.UserFile.user_id == current_user.id).order_by(models.UserFile.upload_time.desc()).all()
     # get all of them files
    return ApiResponse(success=True, data=[
    {"file_key": f.file_key, "filename": f.filename, "uploaded": f.upload_time}
    for f in files # looping through to get all of the files for the JSON response
]) #could be useful in the convo stuff

@router.delete("/files/{file_key}") # to the exact file_key
async def delete_user_file_route(
    file_key: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
): # standard inputs

    file = db.query(models.UserFile).filter(models.UserFile.file_key == file_key).first()
    if not file:
        raise HTTPException(status_code=404, detail="file not found!")
    
    if current_user.id != file.user_id:
        raise HTTPException(status_code=403, detail="Admins only!") # getting the attributes

    db.delete(file)
    db.commit()
    return ApiResponse(success=True, data={"message": "File deleted"})

@router.get("/history", response_model=ApiResponse)
async def get_history(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    sessions = db.query(models.ChatSession).filter(models.ChatSession.user_id == current_user.id).all()

    history_data = []
    for session in sessions:
        entries = db.query(models.Conversation).filter_by(chat_session_id=session.id).order_by(models.Conversation.timestamp).all()
        history_data.append({
            "session_id": session.id,
            "title": session.title,
            "conversations": [
                {
                    "id": c.id,
                    "question": c.question,
                    "answer": c.full_answer,
                    "timestamp": c.timestamp,
                }
                for c in entries
            ]
        })

    return ApiResponse(success=True, data=history_data)

@router.post("/session", response_model=ApiResponse)
async def create_chat_session(title: str = Form(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    session = models.ChatSession(user_id=current_user.id, title=title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return ApiResponse(success=True, data={"session_id": session.id, "title": session.title})

@router.get("/session", response_model=ApiResponse)
async def list_chat_sessions(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    sessions = db.query(models.ChatSession).filter(models.ChatSession.user_id == current_user.id).all()
    return ApiResponse(success=True, data=[{"id": s.id, "title": s.title, "created_at": s.created_at} for s in sessions])

@router.get("/session/{session_id}", response_model=ApiResponse)
async def get_conversation_by_session(session_id: int, db: Session =Depends(get_db), current_user: models.User = Depends(get_current_user)):
    entries = db.query(models.Conversation).filter(
        models.Conversation.user_id == current_user.id,
        models.Conversation.chat_session_id ==session_id
    ).order_by(models.Conversation.timestap.asc()).all()

    return ApiResponse(success=True, data=[
            { 
            "id": c.id,
            "question": c.question,
            "answer": c.full_answer,
            "timestamp": c.timestamp
        } for c in entries
    ])

@router.delete("/session/{session_id}")
async def delete_chat_session(session_id: int, db: Session= Depends(get_db), current_user: models.User = Depends(get_current_user)):
    session = db.query(models.ChatSession).filter_by(id=session_id, user_id=current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found bro!")
    db.delete(session)
    db.commit
    return ApiResponse(success=True, data={"message": "Session deleted"})