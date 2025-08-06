# app/api/routes.py
from fastapi import APIRouter, HTTPException
from app.schemas.meal_plan import MealPlanRequest
from app.services import gemini_service

# Create an API router
router = APIRouter()

@router.post("/api/generate", tags=["Meal Plan"])
async def generate_meal_plan_endpoint(request: MealPlanRequest):
    """
    Receives user preferences and generates a meal plan.
    This endpoint handles the web request and response.
    """
    try:
        # Call the service layer to do the actual work
        meal_plan = gemini_service.generate_meal_plan_from_gemini(request)
        return meal_plan
    except Exception as e:
        # If anything goes wrong in the service, catch it here
        print(f"An error occurred in the API endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate meal plan.")

@router.get("/", tags=["Status"])
def read_root():
    """A simple endpoint to check if the backend is running."""
    return {"message": "AI Meal Planner backend is running!"}