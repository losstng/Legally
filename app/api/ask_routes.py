from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas.ask import AskRequest, QAResponse, AskResponse, HistoryResponseItem
from app.utils.security import get_current_user
from datetime import datetime
from app.utils.redis import redis_client


router = APIRouter()


@router.post("/", response_model=QAResponse)
async def ask_question(
   data: AskRequest,
   db: Session = Depends(get_db),
   current_user: models.User = Depends(get_current_user)
):
   # Placeholder for AI logic or answer retrieval
   answer = f"This is a placeholder response to: '{data.question}'"


   conversation = models.Conversation(question=data.question, answer=answer)
   db.add(conversation)
   db.commit()
   db.refresh(conversation)


   return conversation


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
   question_text = request.question

   cached_answer = redis_client.get(f"qa:{question_text}")
   if cached_answer:
      return AskResponse(question=question_text, answer=cached_answer)

   # Placeholder logic for now
   answer = "Your question has been received and will be reviewed."

   #store answer in Redis and control memory usage with TTL
   redis_client.setex(f"qa:{question_text}", 3600, answer)

   #saved to database
   new_convo = models.Conversation(
       user_id=current_user.id,
       question=question_text,
       answer=answer,
       timestamp=datetime.utcnow()
   )
   db.add(new_convo)
   db.commit()
   db.refresh(new_convo)


   return AskResponse(
       question=new_convo.question,
       answer=new_convo.answer
   )


# GET /history
@router.get("/history", response_model=list[HistoryResponseItem])
async def get_history(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
   conversations = db.query(models.Conversation).filter(models.Conversation.user_id == current_user.id).order_by(models.Conversation.timestamp.desc()).all()
  
   return [
       HistoryResponseItem(
           id=convo.id,
           question=convo.question,
           answer=convo.answer,
           timestamp=convo.timestamp
       ) for convo in conversations
   ]


