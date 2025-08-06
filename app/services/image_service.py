import google.generativeai as genai

# Initialize the model specifically for image generation
# NOTE: Ensure the model name is one you have access to for image generation.
# 'gemini-1.5-pro' is a powerful multimodal model capable of this.
image_model = genai.GenerativeModel('gemini-1.5-pro')

def generate_image_from_prompt(prompt: str) -> bytes:
    """
    Generates an image using the Gemini API based on a text prompt.
    Returns the raw image bytes.
    """
    # The prompt for the image model is just the descriptive text
    response = image_model.generate_content(prompt)
    
    # The response for an image generation request contains the image data in parts.
    # We access the raw binary data (bytes) of the first generated image.
    image_bytes = response.parts[0].blob.data
    
    return image_bytes