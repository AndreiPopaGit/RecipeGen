# app/services/gemini_service.py
import json
import google.generativeai as genai
from app.schemas.meal_plan import MealPlanRequest, SINGLE_DISH_OUTPUT_SCHEMA

# Configure the generation settings once
generation_config = genai.types.GenerationConfig(
    response_mime_type="application/json",
    response_schema=SINGLE_DISH_OUTPUT_SCHEMA,
)

# Initialize the model once
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def generate_meal_plan_from_gemini(request: MealPlanRequest) -> dict:
    """
    Generates a single dish recommendation using the Gemini API.
    """
    # This new prompt is tailored for a single dish and handles optional inputs gracefully.
    prompt = f"""
        You are an expert nutritionist and creative chef.
        Your task is to generate a single, delicious, and balanced dish recipe based on the user's specific needs.

        Here are the user's preferences:
        - Main Goal: {request.mainGoal}
        - Specific Diets to Follow: {', '.join(request.specificDiet) if request.specificDiet else "None provided"}
        - Cuisines they are in the mood for: {', '.join(request.cuisines) if request.cuisines else "Any"}
        - Maximum Cooking Time: {request.cookingTime if request.cookingTime else "Not specified"}
        - Ingredients they like: {request.likedIngredients if request.likedIngredients else "None"}
        - Ingredients they dislike: {request.dislikedIngredients if request.dislikedIngredients else "None"}

        Based on the information above, create a recipe. Your response must be a perfectly structured JSON object.
        You need to provide:
        - An enticing "dishName".
        - A short, appealing "description" of the meal.
        - An approximate "calories" count for a single serving.
        - A list of all "ingredients".
        - A list of step-by-step "instructions", where each step is a separate item in the list.
        
    """

    # Call the Gemini API
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    return json.loads(response.text)