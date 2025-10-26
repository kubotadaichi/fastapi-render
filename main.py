from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware # 追加
import base64

from mutagen.mp3 import MP3

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
    speed: float = 1.0  # 音声速度のパラメータ
    actor: str = 'masumoto'  # 音声アクターのパラメータ（デフォルト: masumoto）

@app.get("/")
def read_root():
    return {"message": "Hello, Render!"}

@app.post("/api/answer")
def answer(req: AnswerRequest):
    text = req.text
    # Gemini APIを呼び出して回答を取得

    dori_f = False
    if "/dori" == text[0:5]:
        text = text[5:]
        dori_f = True

    answer, url, start_time, feeling_id = get_answer_from_gemini(text)

    speed = req.speed
    actor = req.actor
    
    print(f"Received request - actor: {actor}, speed: {speed}")

    # アクターに応じてmodel_idを設定
    if actor == 'dori' or dori_f:
        model_id = 'e143eae381414aeaa0f2a29dc8b5c9f2'
    elif actor == 'masumoto':
        model_id = '7649fdd17d9344648375343b203120f5'
    elif actor == 'kubota':
        model_id = 'c906b79a1bd740f2897e4311eb58d203'
    else:
        model_id = '7649fdd17d9344648375343b203120f5'  # デフォルト: masumoto
    
    print(f"Selected model_id: {model_id} for actor: {actor}")

    response = {
        "answer": answer,
        "video_url": url,
        "start_time": start_time,
        "feeling_id": feeling_id
    }
    
    # 音声生成が要求された場合
    if req.include_audio:
        try:
            # 音声を生成
            audio_data = generate_tts_to_bytes(answer, speed=speed, model_id=model_id)
            
            if audio_data:
                # Base64エンコード
                audio = MP3(r"cloned_voice.mp3")
                length = audio.info.length
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                response["audio"] = {
                    "data": audio_base64,
                    "format": "mp3",
                    "mime_type": "audio/mpeg",
                    "length": length * 1000  # ミリ秒単位
                }
            
        except Exception as e:
            print(f"Audio generation error: {e}")
            response["audio_error"] = str(e)
    
    return response
