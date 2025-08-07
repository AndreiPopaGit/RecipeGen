# app/services/image_service.py
import os
import re
import datetime
import google.generativeai as genai
from google.generativeai import types

# --- CRITICAL NOTE ON THE MODEL ---
# The script you provided uses a model that is NOT in your list of available models.
# Using 'gemini-2.0-flash-preview-image-generation' will likely fail.
# I have used 'gemini-1.5-flash' from your list below.
# You can try swapping it, but 'gemini-1.5-flash' is confirmed to be available to you.
MODEL_NAME = 'gemini-1.5-flash'

# Helper function to create a safe filename
def _create_safe_filename(prompt: str) -> str:
    prompt_slug = re.sub(r'[^\w\s-]', '', prompt).strip().lower()
    prompt_slug = re.sub(r'[\s_-]+', '-', prompt_slug)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{prompt_slug[:50]}-{timestamp}.png"

def generate_image_from_prompt(prompt: str) -> bytes:
    """
    Generates an image using the Gemini API, saves it locally,
    and returns the raw image bytes using the Client() pattern.
    """
    # This uses the lower-level Client API, as seen in your example.
    # It assumes genai.configure(api_key=...) has already been called.
    client = genai.Client()

    # Create the full prompt for the model
    full_prompt = f"Generate a high-quality, photorealistic image of: {prompt}"

    # Use the corrected GenerationConfig class
    config = types.GenerationConfig(
      response_modalities=['IMAGE']
    )

    # Make the API call using the client.models.generate_content method
    response = client.models.generate_content(
        model=f"models/{MODEL_NAME}",
        contents=full_prompt,
        generation_config=config
    )

    # Iterate through the response to find the image data, as per your example
    image_bytes = None
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            image_bytes = part.inline_data.data
            break

    if not image_bytes:
        raise ValueError("Could not extract image data from the response. The model may have returned text instead.")

    # Save the image locally
    try:
        output_dir = "generated_images"
        os.makedirs(output_dir, exist_ok=True)
        filename = _create_safe_filename(prompt)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(image_bytes)
        
        print(f"Successfully saved image to: {filepath}")

    except Exception as e:
        print(f"Error saving image locally: {e}")

    # Return the image bytes to the API route
    return image_bytes