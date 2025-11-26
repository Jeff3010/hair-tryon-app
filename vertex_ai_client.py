import requests
import base64
import json
from typing import Optional, Dict, Any
import google.generativeai as genai
from PIL import Image
import io

class VertexAIHairTransfer:
    """
    Client for Google Vertex AI / Gemini API to perform hair style transfer
    using Gemini 2.0 Flash model for image generation
    """
    
    def __init__(self):
        # Configure Gemini with your Google AI Studio API key
        self.api_key = "AIzaSyCQQ8-NGgeequPtR9FsMnU0SNAbg6LFiYw"
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 2.5 Flash Image for image understanding and vision tasks
        self.model = genai.GenerativeModel('gemini-2.5-flash-image')
        
    def load_image(self, image_path: str) -> Image.Image:
        """Load image from file path"""
        return Image.open(image_path)
    
    def hair_transfer(self, 
                     user_image_path: str, 
                     hairstyle_image_path: str,
                     prompt_override: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform hair style transfer from reference image to user photo
        
        Args:
            user_image_path: Path to the user's photo
            hairstyle_image_path: Path to the reference hairstyle photo
            prompt_override: Optional custom prompt
            
        Returns:
            API response with the generated content
        """
        
        try:
            # Load images
            user_image = self.load_image(user_image_path)
            hairstyle_image = self.load_image(hairstyle_image_path)
            
            # Detailed prompt for hair transfer
            default_prompt = """
            You are an expert AI image analyst and stylist. Analyze these two images:
            
            Image 1 (User Photo): The person who wants to try a new hairstyle
            Image 2 (Reference Hairstyle): The hairstyle to be applied
            
            Task: Describe in extreme detail how to perform a virtual hair try-on that would:
            
            1. PRESERVE COMPLETELY (from Image 1):
               - All facial features exactly as they are (eyes, nose, mouth, face shape)
               - Skin tone and texture
               - Body position and clothing
               - Background
               - Any distinguishing marks or features
               - The person's age and gender
            
            2. TRANSFER (from Image 2):
               - Overall hairstyle shape and volume
               - Hair texture (straight/wavy/curly)
               - Hair length
               - Bangs or fringe style
               - Hair parting
               - Hair flow and movement
            
            3. ENSURE NATURAL INTEGRATION:
               - The hairstyle should look natural on the person
               - Hair color should complement the person's skin tone
               - Proper shadows and lighting
               - Seamless blend at the hairline
            
            Provide a detailed description of what the final result would look like, describing the person from Image 1 with the hairstyle from Image 2 applied naturally and realistically.
            
            Then, generate a step-by-step guide for how an image editor would create this transformation while maintaining photorealistic quality.
            """
            
            prompt = prompt_override if prompt_override else default_prompt
            
            # Generate response using Gemini
            response = self.model.generate_content([
                prompt,
                user_image,
                hairstyle_image
            ])
            
            # Return the response
            return {
                "status": "success",
                "description": response.text,
                "safety_ratings": response.safety_ratings if hasattr(response, 'safety_ratings') else None
            }
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def generate_transformation_guide(self, result: Dict[str, Any]) -> str:
        """
        Extract transformation guide from the result
        
        Args:
            result: API response containing the analysis
            
        Returns:
            Formatted transformation guide
        """
        if "status" == "success" and "description" in result:
            return result["description"]
        return "Unable to generate transformation guide"