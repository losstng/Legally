from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas.ask import AskRequest, QAResponse, AskResponse, HistoryResponseItem
from app.utils.security import get_current_user
from datetime import datetime
from app.utils.redis import redis_client
from app.services.llm import ask_legal_question_with_context, get_limited_context
from app.services.vector_store import retrieve_relevant_chunks
from app.services.agents import process_legal_question

router = APIRouter() #an extension of taking different routes for the api, rahter than calling the app directly


@router.post("/ask", response_model=AskResponse)
async def ask_question( #letting fastapi know that we are going to use async where it is single thread but efficient
   
   request: AskRequest,
   db: Session = Depends(get_db),
   current_user: models.User = Depends(get_current_user)
):  
   question_text = request.question  # <-- define it here
   
   cached_answer = redis_client.get(f"qa:{question_text}") #f stands for formatted string 
   if cached_answer:
      return AskResponse(question=question_text, answer=cached_answer)

   context_str = get_limited_context(question_text)

   
   # Placeholder logic for now
   base_answer = ask_legal_question_with_context(question_text, context_str)
   
   full_answer = process_legal_question(question_text, context_str, base_answer)
   
   # Store answer in Redis (abstract here)
   redis_client.setex(f"qa:{question_text}", 3600, full_answer) #set expiry for the prompt that is being cached for efficiency
    #save in a dictionary format, question text (qa) as key, and answer as value
   # Save to database
   new_convo = models.Conversation(
       user_id=current_user.id,
       question=question_text,
       base_answer=base_answer,
       full_answer=full_answer,
       timestamp=datetime.utcnow()
   )
   db.add(new_convo)
   db.commit()
   db.refresh(new_convo)

   return AskResponse(
       question=new_convo.question,
       answer=new_convo.full_answer
   )


# GET /history
@router.get("/history", response_model=list[HistoryResponseItem])
async def get_history(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
   conversations = db.query(models.Conversation).filter(models.Conversation.user_id == current_user.id).order_by(models.Conversation.timestamp.desc()).all()
  #these '.' are there to add like adjective for it yk
   return [
       HistoryResponseItem(
           id=convo.id,
           question=convo.question,
           answer=convo.answer,
           timestamp=convo.timestamp
       ) for convo in conversations
   ]


