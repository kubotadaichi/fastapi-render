from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware # 追加
import base64

from src.gemini import get_answer_from_gemini
from audio.fishaudio import generate_tts_to_bytes

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
    include_audio: bool = False  # 音声を含めるかどうかのフラグ

@app.get("/")
def read_root():
    return {"message": "Hello, Render!"}

@app.post("/api/answer")
def answer(req: AnswerRequest):
    text = req.text
    # Gemini APIを呼び出して回答を取得
    answer, url, start_time = get_answer_from_gemini(text)
    
    response = {
        "answer": answer,
        "video_url": url,
        "start_time": start_time
    }
    
    # 音声生成が要求された場合
    if req.include_audio:
        try:
            # 音声を生成
            audio_data = generate_tts_to_bytes(answer)
            
            if audio_data:
                # Base64エンコード
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                response["audio"] = {
                    "data": audio_base64,
                    "format": "mp3",
                    "mime_type": "audio/mpeg"
                }
            
        except Exception as e:
            print(f"Audio generation error: {e}")
            response["audio_error"] = str(e)
    
    return response
