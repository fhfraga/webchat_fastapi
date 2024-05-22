import logging
from typing import Dict, List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)

messages: Dict[str, List[Dict[str, str]]] = {}

class Message(BaseModel):
    sender: str
    receiver: str
    content: str

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    logging.info("Serving index.html")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send/")
async def send_message(message: Message):
    logging.info(f"Received message from {message.sender} to {message.receiver}: {message.content}")

    if message.sender not in messages:
        messages[message.sender] = []
    if message.receiver not in messages:
        messages[message.receiver] = []

    messages[message.receiver].append({
        "from": message.sender,
        "content": message.content
    })
    return {"status": "Message sent"}

@app.get("/receive/{user}/")
async def receive_messages(user: str):
    logging.info(f"Retrieving messages for {user}")

    if user not in messages:
        messages[user] = []

    user_messages = messages[user]
    #messages[user] = []  # Limpar mensagens depois de recebidas
    return {"messages": user_messages}
