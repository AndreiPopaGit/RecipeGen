# app/schemas/meal_plan.py
from pydantic import BaseModel, conlist

# Schema for the incoming request from the frontend
from typing import List
from pydantic import BaseModel, Field

class MealPlanRequest(BaseModel):
    
    mainGoal: str
    specificDiet: str = ""
    cuisines: List[str] = Field(default_factory=list)
    likedIngredients: str = ""
    dislikedIngredients: str = ""
    cookingTime: str = ""

# The "blueprint" for the Gemini model's single-dish output.
SINGLE_DISH_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "dishName": {
            "type": "string",
            "description": "The name of the recommended meal."
        },
        "description": {
            "type": "string",
            "description": "A short, enticing summary of the dish."
        },
        "calories": {
            "type": "integer",
            "description": "An approximate number of calories for one serving."
        },
        "ingredients": {
            "type": "array",
            "items": {"type": "string"},
            "description": "A list of all ingredients needed for the recipe."
        },
        "instructions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "A list of step-by-step instructions. Each item in the array is a single step."
        }
    },
    "required": ["dishName", "description", "calories", "ingredients", "instructions"]
}