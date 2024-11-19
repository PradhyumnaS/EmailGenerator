from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain import PromptTemplate
from langchain.llms import Clarifai

app = FastAPI()

class EmailRequest(BaseModel):
    sender_name: str
    recipient_name: str
    subject: str
    extra_detail: str
    tone: str
    preferred_length: str
    follow_up: bool = False

class MessageRequest(BaseModel):
    sender_name: str
    recipient_name: str
    message_content: str

def generate_email(sender_name, recipient_name, subject, extra_detail, tone, preferred_length, follow_up):
    PAT = '492e95751129453aafedbdcd9a524186'
    USER_ID = 'meta'
    APP_ID = 'Llama-2'
    MODEL_ID = 'llama2-13b-chat'

    if not follow_up:
        template = f"Generate an email from {sender_name} to {recipient_name} with the following details: " \
                   f"Subject: {subject}. Write it in a {tone} way. Make it {preferred_length} length and add details: {extra_detail}. " \
                   f"Write it in a proper format of a letter."
    else:
        template = f"Generate a follow-up email from {sender_name} to {recipient_name} with a catchy tone. Subject: {subject}. " \
                   f"Politely remind them about the previous email. Mention details: {extra_detail}. Make sure it stands out."

    llm = Clarifai(pat=PAT, user_id=USER_ID, app_id=APP_ID, model_id=MODEL_ID)

    prompt = PromptTemplate(
        input_variables=["sender_name", "recipient_name", "subject", "tone", "preferred_length", "extra_detail"],
        template=template,
    )

    response = llm(prompt.format(
        sender_name=sender_name,
        recipient_name=recipient_name,
        subject=subject,
        tone=tone,
        preferred_length=preferred_length,
        extra_detail=extra_detail
    ))

    return response

@app.post("/generate-email/")
def create_email(email_request: EmailRequest):
    try:
        email_content = generate_email(
            email_request.sender_name, 
            email_request.recipient_name, 
            email_request.subject, 
            email_request.extra_detail, 
            email_request.tone, 
            email_request.preferred_length, 
            email_request.follow_up
        )
        return {"email_content": email_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send-message/")
def send_message(message_request: MessageRequest):
    try:
        message = f"Message from {message_request.sender_name} to {message_request.recipient_name}: {message_request.message_content}"
        return {"message_sent": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

