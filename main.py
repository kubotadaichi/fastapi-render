from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware # 追加


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

class AnswerRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Hello, Render!"}

@app.post("/api/answer")
def answer(req: AnswerRequest):
    text = req.text

    return {"answer": f'「{req.text}」にお答えします！'}