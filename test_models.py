import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")

print("\nTesting gemini-2.5-pro...")
try:
    model = genai.GenerativeModel('gemini-2.5-pro')
    response = model.generate_content("Hello")
    print(f"Success: {response.text}")
except Exception as e:
    print(f"Error with gemini-2.5-pro: {e}")
