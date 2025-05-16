from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload
from uuid import uuid4
from datetime import datetime
from app.db.database import get_db
from app.db import models
from app.db.models import UserFile
from app.schemas.ask import ApiResponse
from app.utils.security import get_current_user
from app.utils.redis import redis_client
from app.services.llm import ask_legal_question_with_context, get_limited_context
from app.services.vector_store import retrieve_relevant_chunks, store_chunks_in_vector_db
from app.services.embedding_loader import load_and_chunk
from app.services.agents import process_legal_question
from app.utils.language import detect_language, SUPPORTED_LANGUAGES
from app.services.files import handle_file_upload, delete_user_file
from app.services.context import get_context_from_file, get_context_from_global, get_context_from_chat_session
from app.services.ask import generate_full_answer
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.DEBUG,  # or INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

router = APIRouter()

# ---------- QUESTION/ANSWER ----------

@router.post("/ask", response_model=ApiResponse)
async def ask_question(
    question: str = Form(...),
    file: UploadFile = File(None),
    file_key: str = Form(None),
    chat_session_id: int = Form(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    session = db.query(models.ChatSession).filter_by(id=chat_session_id, user_id=current_user.id).first()
    if chat_session_id is None:
        raise HTTPException(status_code=400, detail="chat_session_id is required.")
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found.")
    cached_answer = redis_client.get(f"qa:{question}")

    if file:
        file_key = await handle_file_upload(file, current_user.id, db)
        context = await get_context_from_file(file_key, current_user.id, question)
    elif file_key:
        context = await get_context_from_file(file_key, current_user.id, question)
    else:
        context = await get_context_from_global(question)

    if chat_session_id:
        chat_session_context = get_context_from_chat_session(chat_session_id)
        context = f"{chat_session_context}\n\n---\n\n{context}"

    base, full, _ = generate_full_answer(question, context)
    redis_client.setex(f"qa:{question}", 3600, full)

    convo = models.Conversation(
        user_id=current_user.id,
        chat_session_id=chat_session_id,
        question=question,
        base_answer=base,
        full_answer=full
    )
    db.add(convo)
    db.commit()
    db.refresh(convo)

    return ApiResponse(success=True, data={"question": convo.question, "answer": convo.full_answer})

# ---------- SESSIONS ----------

@router.post("/new-session", response_model=ApiResponse)
def create_new_chat_session(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    session = models.ChatSession(user_id=current_user.id, title="Untitled Chat")
    db.add(session)
    db.commit()
    db.refresh(session)
    logger.info(f"New session created: {session.id} by {current_user.email}")
    return ApiResponse(success=True, data={"session_id": session.id})

@router.get("/sessions", response_model=ApiResponse)
def list_chat_sessions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    sessions = db.query(models.ChatSession).filter_by(user_id=current_user.id).all()
    return ApiResponse(success=True, data=[
        {"id": s.id, "title": s.title, "created_at": s.created_at} for s in sessions
    ])

@router.get("/session/{session_id}", response_model=ApiResponse)
def get_conversation_by_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    session = db.query(models.ChatSession).filter_by(id=session_id, user_id=current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    entries = db.query(models.Conversation).filter(
        models.Conversation.user_id == current_user.id,
        models.Conversation.chat_session_id == session_id
    ).order_by(models.Conversation.timestamp.asc()).all()

    return ApiResponse(success=True, data=[
        {
            "id": c.id,
            "question": c.question,
            "answer": c.full_answer,
            "timestamp": c.timestamp,
        } for c in entries
    ])

@router.delete("/session/{session_id}", response_model=ApiResponse)
def delete_chat_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    session = db.query(models.ChatSession).options(joinedload(models.ChatSession.qna_entries)).filter_by(id=session_id, user_id=current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    db.delete(session)
    db.commit()
    return ApiResponse(success=True, data={"message": "Session deleted"})

@router.post("/session/{session_id}/rename", response_model=ApiResponse)
def rename_chat_session(
    session_id: int,
    title: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    session = db.query(models.ChatSession).filter_by(id=session_id, user_id=current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    if len(title.strip()) == 0:
        raise HTTPException(status_code=400, detail="Title cannot be empty.")
    if session.title == title:
        return ApiResponse(success=True, data={"session_id": session.id, "new_title": session.title})
    session.title = title.strip()
    db.commit()
    return ApiResponse(success=True, data={"session_id": session.id, "new_title": session.title})

# ---------- FILES ----------

@router.get("/files", response_model=ApiResponse)
def list_user_files(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    files = db.query(models.UserFile).filter_by(user_id=current_user.id).order_by(models.UserFile.upload_time.desc()).all()
    return ApiResponse(success=True, data=[
        {"file_key": f.file_key, "filename": f.filename, "uploaded": f.upload_time} for f in files
    ])

@router.delete("/files/{file_key}", response_model=ApiResponse)
def delete_user_file_route(
    file_key: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    file = db.query(models.UserFile).filter_by(file_key=file_key).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found.")
    if file.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied.")

    db.delete(file)
    db.commit()
    return ApiResponse(success=True, data={"message": "File deleted"})

@router.post("/files/{file_key}/rename", response_model=ApiResponse)
def rename_uploaded_file(
    file_key: str,
    new_name: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    file = db.query(models.UserFile).filter_by(file_key=file_key, user_id=current_user.id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found.")

    file.filename = new_name
    db.commit()
    return ApiResponse(success=True, data={"file_key": file.file_key, "new_filename": file.filename})

# ---------- HISTORY ----------

@router.get("/history", response_model=ApiResponse)
def get_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    sessions = db.query(models.ChatSession).filter_by(user_id=current_user.id).all()
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
                } for c in entries
            ]
        })

    return ApiResponse(success=True, data=history_data)