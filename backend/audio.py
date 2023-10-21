import openai
from settings import Settings

settings = Settings()
openai.api_key = settings["OPEN_API_KEY"]

def transcribe_audio(audio_bytes : bytes):
    return openai.Audio.transcribe("whisper-1", audio_bytes,
        prompt = settings["WHISPER_AUDIO_PROMPT"]               
    )
