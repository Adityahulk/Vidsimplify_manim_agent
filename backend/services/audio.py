import requests
import os
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def generate_audio(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
    """
    Generates audio from text using ElevenLabs API.
    """
    if not ELEVENLABS_API_KEY:
        print("Warning: ELEVENLABS_API_KEY not set. returning dummy audio.")
        return None

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error generating audio: {response.text}")
        return None
