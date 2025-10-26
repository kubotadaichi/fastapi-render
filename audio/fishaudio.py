import os
import requests
from fish_audio_sdk import Session, TTSRequest, ReferenceAudio
from fish_audio_sdk import Prosody


from dotenv import load_dotenv

load_dotenv()

session = Session(os.getenv("FISH_AUDIO_API_KEY"))

def clone_voice(path):

    # Check account status
    try:
        # Try to get models to verify API access
        models = session.get_models()
        print(f"API access verified. Found {len(models)} existing models.")
    except Exception as e:
        print(f"Warning: Could not verify API access: {e}")

    voices = []
    texts = []
    # Load reference audio
    with open(path, "rb") as f:
            voices.append(f.read())
            texts.append(f"Sample text for reference audio.")

    model = session.create_model(
        title="My Custom Voice",
        description="Voice cloned from samples",
        voices=voices,
        texts=texts,
        visibility="private"  # or "public", "unlist"
    )

    print(f"Created model: {model.id}")

    return model.id

def generate_tts(text, speed, model_id: str='d5219abbc7f048a085bf85aab84ea0ca'):
    # Use the model
    request = TTSRequest(
        text=text,
        reference_id=model_id,
        prosody=Prosody(
            speed=speed,  # 1.2倍速（0.5-2.0の範囲）
        )
    )

    try:
        with open("cloned_voice.mp3", "wb") as f:
            for chunk in session.tts(request,backend="s1"):
                f.write(chunk)
        print("Successfully generated cloned_voice.mp3")
    except Exception as e:
        if "402" in str(e) or "Payment Required" in str(e):
            print("Error: Payment required for Fish Audio TTS service.")
            print("Please check your account balance or upgrade your subscription at https://fish.audio/")
        else:
            print(f"Error generating TTS: {e}")

# def generate_tts_to_bytes(text, speed, model_id: str='85521c2f57da4814a7aefe2ee9e0e9be'):
def generate_tts_to_bytes(text, speed, model_id: str='d5219abbc7f048a085bf85aab84ea0ca'):
    """
    音声を生成してバイト形式で返す関数
    """
    request = TTSRequest(
        text=text,
        reference_id=model_id,
        prosody=Prosody(
            speed=speed,  # 1.2倍速（0.5-2.0の範囲）
    )
    )

    try:
        audio_data = b""
        with open("cloned_voice.mp3", "wb") as f:
            print("Successfully generated audio data")
            for chunk in session.tts(request,backend="s1"):
                audio_data += chunk
                f.write(chunk)
        return audio_data
    except Exception as e:
        if "402" in str(e) or "Payment Required" in str(e):
            print("Error: Payment required for Fish Audio TTS service.")
            print("Please check your account balance or upgrade your subscription at https://fish.audio/")
        else:
            print(f"Error generating TTS: {e}")
        return None

if __name__ == "__main__":

    path = "data/audio/ドリー.mp3"

    # path = "data/.mp3"audio/監督.mp3"
    print(clone_voice(path))