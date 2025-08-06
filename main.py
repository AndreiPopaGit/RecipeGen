# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

# Import settings and the API router from our new app structure
from app.config import settings
from app.api.routes import router

# --- INITIALIZATION ---
app = FastAPI(
    title="AI Meal Planner API",
    description="API for generating personalized meal plans using Google Gemini.",
    version="1.0.0"
)

# Configure the Gemini API client using the key from our config
genai.configure(api_key=settings.GEMINI_API_KEY)

# --- CORS MIDDLEWARE ---
# Allows the frontend (e.g., at http://localhost:3000) to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INCLUDE ROUTER ---
# This line tells the main FastAPI app to use the routes defined in app/api/routes.py
app.include_router(router)