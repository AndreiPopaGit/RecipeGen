# app/api/routes.py
from fastapi import APIRouter, HTTPException,Response
from app.schemas.meal_plan import MealPlanRequest
from app.schemas.image_request import ImageRequest
from app.services import gemini_service
from app.services import image_service

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
    
# +++ IMAGE GENERATION ENDPOINT (New) +++
@router.post("/api/generate-image", tags=["Image Generation"])
async def generate_image_endpoint(request: ImageRequest):
    """
    Generates an image based on a text prompt.
    """
    try:
        # Call the image service to get the image bytes
        image_bytes = image_service.generate_image_from_prompt(request.prompt)
        
        # Return the bytes directly as a response with the correct media type
        return Response(content=image_bytes, media_type="image/png")
    except Exception as e:
        print(f"An error occurred in the image generation endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate image.")

@router.get("/", tags=["Status"])
def read_root():
    """A simple endpoint to check if the backend is running."""
    return {"message": "AI Meal Planner backend is running!"}