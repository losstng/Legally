from app.services.vector_store import load_vector_db, retrieve_relevant_chunks
from app.db.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
import logging
from app.db import models
from sqlalchemy import desc

logger = logging.getLogger(__name__)
async def get_context_from_file(file_key: str, user_id: int, question: str) -> str:
    vector_path = f"db/faiss_user_{user_id}_{file_key}"
    logger.info(f"[RETRIEVAL] Loading vector DB from: {vector_path}")

    db = load_vector_db(vector_path)
    results = db.similarity_search_with_score(question, k=10)
    logger.info(f"[RETRIEVAL] Retrieved {len(results)} chunks")

    for i, (doc, score) in enumerate(results):
        content = getattr(doc, "page_content", None)
        if content:
            logger.debug(f"[MATCH {i+1}] Score: {score:.4f} | Chunk: {content[:200]!r}")
        else:
            logger.warning(f"[MATCH {i+1}] Score: {score:.4f} | Chunk: [EMPTY OR INVALID DOCUMENT]")
    
    return "\n\n".join([
        doc.page_content for doc, score in results
        if getattr(doc, "page_content", "").strip()
    ])

async def get_context_from_global(question: str, max_tokens=1500) -> str: 
    return retrieve_relevant_chunks(question, k=10)  # Already token-limited


async def get_context_from_chat_session(session_id: int, db: Session=Depends(get_db)) -> str:
    past_convos = (
        db.query(models.Conversation)
        .filter(models.Conversation.chat_session_id == session_id)
        .order_by(desc(models.Conversation.timestamp))
        .limit(5)
        .all()
    )

    context_blocks = [
        f"User: {conv.question}\nBot: {conv.base_answer}"
        for conv in reversed(past_convos)  # so it reads oldest to newest
    ]

    return "\n\n".join(context_blocks)