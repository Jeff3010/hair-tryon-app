import google.generativeai as genai
from PIL import Image
import io
import base64
from typing import Optional, Dict, Any
import json

class HairTransformAI:
    """
    Client for Google Gemini API to perform hair style transfer
    Generates actual transformed images
    """
    
    def __init__(self):
        # Configure Gemini with your Google AI Studio API key
        self.api_key = "AIzaSyCQQ8-NGgeequPtR9FsMnU0SNAbg6LFiYw"
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 2.0 Flash Image Generation for actual image generation
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
        
    def load_image(self, image_path: str) -> Image.Image:
        """Load image from file path"""
        return Image.open(image_path)
    
    def hair_transfer(self, 
                     user_image_path: str, 
                     hairstyle_image_path: str,
                     prompt_override: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform hair style transfer - generate new image with hairstyle applied
        
        Args:
            user_image_path: Path to the user's photo
            hairstyle_image_path: Path to the reference hairstyle photo
            prompt_override: Optional custom prompt
            
        Returns:
            Dictionary with generated image and status
        """
        
        try:
            # Load images
            user_image = self.load_image(user_image_path)
            hairstyle_image = self.load_image(hairstyle_image_path)
            
            # Optimized prompt for salon styling visualization
            default_prompt = """
            Create a professional hair styling visualization for salon consultation purposes.
            
            Context: This is a legitimate hair salon styling tool to help customers visualize different hairstyles before making a decision. This is for professional beauty consultation only.
            
            Task: Create a styling visualization that shows how a hairstyle would look.
            
            Input Analysis:
            - Image 1: Customer portrait for professional styling consultation
            - Image 2: Reference hairstyle from a style catalog
            
            Professional Styling Requirements:
            1. Maintain the customer's natural appearance and characteristics
            2. Demonstrate how the reference hairstyle would adapt to their features
            3. Create a professional salon-quality visualization
            4. Show realistic hair texture and movement
            5. Ensure natural color adaptation for their complexion
            
            Output: A professional styling visualization suitable for salon consultation, showing the proposed hairstyle in a realistic and helpful manner for the customer's styling decision.
            
            Note: This is exclusively for professional beauty consultation and helping customers make informed styling choices at a licensed salon.
            """
            
            prompt = prompt_override if prompt_override else default_prompt
            
            # Generate image using Gemini
            response = self.model.generate_content([prompt, user_image, hairstyle_image])
            
            # Extract the generated image from response
            result = {
                "status": "success",
                "response": response,
                "generated_image": None
            }
            
            # Check if response contains an image
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        # Check for image data in the response
                        if hasattr(part, 'inline_data') and part.inline_data:
                            if hasattr(part.inline_data, 'data'):
                                # Image data found
                                image_data = part.inline_data.data
                                mime_type = part.inline_data.mime_type if hasattr(part.inline_data, 'mime_type') else 'image/png'
                                
                                # Convert to PIL Image
                                image = Image.open(io.BytesIO(base64.b64decode(image_data)))
                                result["generated_image"] = image
                                result["mime_type"] = mime_type
                                break
                        elif hasattr(part, 'text'):
                            # If only text is returned, it means image generation wasn't successful
                            result["text_response"] = part.text
                            
            # If no image was generated, try to provide helpful information
            if not result.get("generated_image") and result.get("text_response"):
                result["status"] = "text_only"
                result["message"] = "The model returned analysis instead of an image. This might be due to safety filters or model limitations."
                
            return result
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def save_generated_image(self, result: Dict[str, Any], output_path: str) -> bool:
        """
        Save the generated image to a file
        
        Args:
            result: Result dictionary from hair_transfer
            output_path: Path to save the image
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            if result.get("generated_image"):
                result["generated_image"].save(output_path)
                return True
            return False
        except Exception as e:
            print(f"Error saving image: {e}")
            return False