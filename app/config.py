# app/config.py
import os
from dotenv import load_dotenv

# Load environment variables from a .env file at the project root
load_dotenv()

class Settings:
    """Holds all application settings."""
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

settings = Settings()

# Basic check to ensure the key was loaded
if not settings.GEMINI_API_KEY:
    print("FATAL ERROR: GEMINI_API_KEY not found in .env file.")
    exit(1)