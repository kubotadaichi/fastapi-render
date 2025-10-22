from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware # 追加

app = FastAPI()

# CORSを回避するために追加（今回の肝）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

app = FastAPI()

@app.get("/")
def read_root():
	return {"message" : "Hello, Render!"}

@app.post("/api/answer")
def answer(text: str):
	return {"text": text}