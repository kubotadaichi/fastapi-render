from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware # 追加

from src.gemini import get_answer_from_gemini

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
	# Gemini APIを呼び出して回答を取得
	answer, url = get_answer_from_gemini(text)
     
	return {
          "answer": answer,
          "video_url": url
          }