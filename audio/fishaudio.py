import os
import requests
from fish_audio_sdk import Session, TTSRequest, ReferenceAudio

from dotenv import load_dotenv

load_dotenv()


session = Session(os.getenv("FISH_AUDIO_API_KEY"))

def clone_voice():

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
    with open("data/audio/監督.mp3", "rb") as f:
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

def generate_tts(text, model_id: str='d5219abbc7f048a085bf85aab84ea0ca'):
    # Use the model
    request = TTSRequest(
        text=text,
        reference_id=model_id,
    )

    try:
        with open("cloned_voice.mp3", "wb") as f:
            for chunk in session.tts(request):
                f.write(chunk)
        print("Successfully generated cloned_voice.mp3")
    except Exception as e:
        if "402" in str(e) or "Payment Required" in str(e):
            print("Error: Payment required for Fish Audio TTS service.")
            print("Please check your account balance or upgrade your subscription at https://fish.audio/")
        else:
            print(f"Error generating TTS: {e}")

def generate_tts_to_bytes(text, model_id: str='d5219abbc7f048a085bf85aab84ea0ca'):
    """
    音声を生成してバイト形式で返す関数
    """
    request = TTSRequest(
        text=text,
        reference_id=model_id,
    )

    try:
        audio_data = b""
        for chunk in session.tts(request):
            audio_data += chunk
        print("Successfully generated audio data")
        return audio_data
    except Exception as e:
        if "402" in str(e) or "Payment Required" in str(e):
            print("Error: Payment required for Fish Audio TTS service.")
            print("Please check your account balance or upgrade your subscription at https://fish.audio/")
        else:
            print(f"Error generating TTS: {e}")
        return None

if __name__ == "__main__":

    generate_tts('こんにちは！増本 浩平（ますもと こうへい）です！神奈川県藤沢市出身の元サッカー選手で、今はサッカー指導者をしています。現役時代のポジションはDFとFWでした。サッカーのことなら何でも聞いてください！もう、話したくてうずうずしていますよ！\n\nせっかくなので、サッカーの試合の雰囲気を感じられる動画を紹介しますね。この動画は、ギラヴァンツのサポーターが試合の準備をしているシーンです。スタジアムの雰囲気やサポーターの応援の様子がよくわかりますよ！\n動画はこちらです！')