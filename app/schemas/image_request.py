from pydantic import BaseModel

class ImageRequest(BaseModel):
    """
    Schema for the incoming request for image generation.
    """
    prompt: str