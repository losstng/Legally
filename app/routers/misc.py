from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, constr
from app.schemas.ask import ApiResponse
import logging
import smtplib
from email.message import EmailMessage
import os

router = APIRouter()

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: constr(min_length=1)
    message: constr(min_length=1)

@router.post("/contact", response_model=ApiResponse)
async def send_contact_form(payload: ContactForm):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Contact Form — {payload.subject}"
        msg["From"] = payload.email
        msg["To"] = "long131005@gmail.com"
        msg.set_content(f"From: {payload.name} <{payload.email}>\n\n{payload.message}")

        with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465) as smtp:
            smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(msg)

        logging.info(f"Contact form submitted: {payload.email}")
        return ApiResponse(success=True, data={"message": "Message sent successfully."})
    except Exception as e:
        logging.error(f"Email sending failed: {e}")
        raise HTTPException(status_code=500, detail="Could not send message.")