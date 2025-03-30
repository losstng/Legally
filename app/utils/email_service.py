import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import logging
load_dotenv()
#Email Configuration
SMTP_SERVER = "smtp.mail.yahoo.com"  #set up
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("EMAIL_ADDRESS")  #from my email
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD") #unlikely to work as it usually requires OTP

def send_otp_email(recipient_email, otp):   #defining this function execute
    subject = "Your OTP Code" 
    body = f"Your One-Time Password (OTP) is: {otp}. It will expire in 5 minutes."

        #MIME stands for Multipurpose Internet Mail Extensions
    msg = MIMEText(body) #SMTP servers expect emails to follow the MIME format (Multipurpose Internet Mail Extensions) and this is a format which always include subject, from, and to, as defined above
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:  #this is a function to execute sending mail through the function
            server.starttls()  #Secure the connection through transfer layer security
            server.login(SENDER_EMAIL, SENDER_PASSWORD) #login
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string()) #and sending the email as simple as that, and the msg will be occupied and distributed by the SMTP
        print(f"✅ OTP sent successfully to {recipient_email}") 
    except Exception as e:
        logging.error(f"Error sending OTP to {recipient_email}: {e}") # this could be a problem when something doesn't work, a fallback system

