# list_models.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file.")
else:
    genai.configure(api_key=api_key)

    print("--- Available Models ---")
    for model in genai.list_models():
        # Check if 'generateContent' is one of the supported methods for the model
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")
    print("------------------------")