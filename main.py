import json

import redis
from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    chat_id = "default_chat"
    
    messages = [json.loads(msg) for msg in r.lrange(chat_id, 0, -1)]
    await websocket.send_text(json.dumps({"messages": messages}))
    
    while True:
        data = await websocket.receive_text()
        message = json.loads(data)
        
        r.lpush(chat_id, json.dumps(message))

        await websocket.send_text(json.dumps(message))
