# app/api/routes.py
import logging
from fastapi import APIRouter, HTTPException, Response
from app.schemas.meal_plan import MealPlanRequest
from app.schemas.image_request import ImageRequest
from app.services import gemini_service
from app.services import image_service

# --- Setup a proper logger ---
# This will give you detailed error messages in your console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an API router
router = APIRouter()

# --- MEAL PLAN ENDPOINT ---
@router.post("/api/generate", tags=["Meal Plan"])
async def generate_meal_plan_endpoint(request: MealPlanRequest):
    """
    Receives user preferences and generates a meal plan.
    """
    try:
        logger.info("Generating meal plan...")
        meal_plan = gemini_service.generate_meal_plan_from_gemini(request)
        logger.info("Successfully generated meal plan.")
        return meal_plan
    except Exception as e:
        # This will now log the FULL error traceback to your console
        logger.error(f"An error occurred in /api/generate endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate meal plan.")

# --- IMAGE GENERATION ENDPOINT ---
@router.post("/api/generate-image", tags=["Image Generation"])
async def generate_image_endpoint(request: ImageRequest):
    """
    Generates an image based on a text prompt.
    """
    try:
        logger.info(f"Generating image with prompt: {request.prompt[:50]}...")
        image_bytes = image_service.generate_image_from_prompt(request.prompt)
        logger.info("Successfully generated image.")
        return Response(content=image_bytes, media_type="image/png")
    except Exception as e:
        # This will now log the FULL error traceback to your console
        logger.error(f"An error occurred in /api/generate-image endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate image.")

# --- STATUS ENDPOINT ---
@router.get("/", tags=["Status"])
def read_root():
    """A simple endpoint to check if the backend is running."""
    return {"message": "AI Meal Planner backend is running!"}