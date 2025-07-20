import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, conlist
import google.generativeai as genai

# Load environment variables from a .env file
load_dotenv()

# --- INITIALIZATION ---
app = FastAPI()

# Initialize only the Gemini API client
try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except KeyError:
    print("ERROR: GEMINI_API_KEY not found. Please check your .env file.")
    exit(1)

# --- CORS MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA VALIDATION MODEL ---
class MealPlanRequest(BaseModel):
    userGoal: str
    people: str
    preferences: conlist(str) # No need for min_length if you trust the frontend
    wantLeftovers: str
    dailyBudget: str
    specialRequests: str


# --- API ROUTES ---
@app.post("/api/generate")
async def generate_meal_plan(request: MealPlanRequest):
    """Receives user preferences and generates a meal plan using Gemini."""
    try:
        prompt = f"""
            Create a detailed, personalized meal plan based on these preferences:
            - Goal: {request.userGoal}
            - Cooking for: {request.people}
            - Dietary Preferences: {', '.join(request.preferences)}
            - Wants Leftovers: {request.wantLeftovers}
            - Daily Budget: ${request.dailyBudget}
            - Special Requests: {request.specialRequests}

            Return the meal plan as a structured JSON object. For example:
            {{ "breakfast": {{ "name": "...", "ingredients": [...] }}, "lunch": ..., "dinner": ... }}
        """

        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return {"mealPlan": response.text}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate meal plan.")

@app.get("/")
def read_root():
    return {"message": "AI Meal Planner backend is running!"}