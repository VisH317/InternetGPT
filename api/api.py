import os
from chat import Chat
from fastapi import FastAPI

key = os.getenv("OPENAI_KEY")

# params
max_similar = 10

app = FastAPI()
chat = Chat(key, "")

@app.get("/set-prompt")
def set_prompt(prompt: str = ""):
    if len(prompt)!=0: chat.change_prompt(prompt)
    return {"success": True}

@app.get("/question")
def ask(question: str = ""):
    res = chat.query(question, max_similar)
    return res



