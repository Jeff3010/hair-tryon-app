import google.generativeai as genai
from PIL import Image
import io
import base64
from typing import Optional, Dict, Any
import json

class TextBasedHairTransform:
    """
    Client for Google Gemini API to perform hair style transformation
    using text descriptions instead of reference images
    """
    
    def __init__(self):
        # Configure Gemini with your Google AI Studio API key
        self.api_key = "AIzaSyCQQ8-NGgeequPtR9FsMnU0SNAbg6LFiYw"
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 2.0 Flash for image generation
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
        
    def load_image(self, image_path: str) -> Image.Image:
        """Load image from file path"""
        return Image.open(image_path)
    
    def generate_with_text_description(self, 
                                      user_image_path: str, 
                                      hairstyle_description: str,
                                      additional_details: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate new hairstyle based on text description
        
        Args:
            user_image_path: Path to the user's photo
            hairstyle_description: Text description of desired hairstyle
            additional_details: Optional additional styling details
            
        Returns:
            Dictionary with generated image and status
        """
        
        try:
            # Load user image
            user_image = self.load_image(user_image_path)
            
            # Create comprehensive prompt
            prompt = f"""
            Professional Salon Styling Request:
            
            Task: Create a professional hair styling visualization based on the following specifications.
            
            Customer has requested this hairstyle:
            {hairstyle_description}
            
            Additional styling preferences:
            {additional_details if additional_details else "Natural adaptation to suit the customer's features"}
            
            Professional Requirements:
            - This is for a licensed salon consultation
            - Show how the requested hairstyle would look professionally styled
            - Maintain the customer's natural facial features
            - Ensure the style looks realistic and achievable
            - Professional salon-quality visualization
            
            Create a styling visualization showing the requested hairstyle.
            """
            
            # Generate image using Gemini
            response = self.model.generate_content([prompt, user_image])
            
            # Extract the generated result
            result = {
                "status": "success",
                "response": response,
                "generated_image": None
            }
            
            # Process response to extract image if available
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, 'inline_data') and part.inline_data:
                            if hasattr(part.inline_data, 'data'):
                                image_data = part.inline_data.data
                                mime_type = part.inline_data.mime_type if hasattr(part.inline_data, 'mime_type') else 'image/png'
                                
                                # Convert to PIL Image
                                image = Image.open(io.BytesIO(base64.b64decode(image_data)))
                                result["generated_image"] = image
                                result["mime_type"] = mime_type
                                break
                        elif hasattr(part, 'text'):
                            result["text_response"] = part.text
                            
            return result
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def save_generated_image(self, result: Dict[str, Any], output_path: str) -> bool:
        """Save the generated image to a file"""
        try:
            if result.get("generated_image"):
                result["generated_image"].save(output_path)
                return True
            return False
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

# Predefined hairstyle templates for easy selection
HAIRSTYLE_TEMPLATES = {
    "Bob Cut": "Classic bob haircut, chin-length, straight edges, professional and elegant",
    "Pixie Cut": "Short pixie cut, textured layers, modern and edgy style",
    "Long Layers": "Long layered hair, flowing layers, natural movement, shoulder-length or longer",
    "Beach Waves": "Beachy wavy hair, loose natural waves, casual and effortless look",
    "Sleek Straight": "Perfectly straight hair, smooth and shiny, professional appearance",
    "Curly/Afro": "Natural curly or afro-textured hair, voluminous and defined curls",
    "Undercut": "Modern undercut style, short on sides, longer on top, contemporary look",
    "Shoulder Length": "Medium length hair to shoulders, versatile styling, professional",
    "Bangs/Fringe": "Hair with bangs or fringe, can specify straight, side-swept, or curtain bangs",
    "Updo/Bun": "Hair styled up in a bun or updo, elegant and formal styling",
    "Braided": "Braided hairstyle, can be box braids, cornrows, or french braids",
    "Vintage Wave": "Vintage Hollywood waves, glamorous retro styling",
    "Shag Cut": "Layered shag haircut, textured and rock-inspired",
    "Lob (Long Bob)": "Long bob haircut, collarbone length, modern and sophisticated",
    "Side Part": "Hair with defined side parting, classic professional style",
    "Center Part": "Hair with center parting, symmetrical and balanced",
    "Mohawk/Faux Hawk": "Edgy mohawk or faux hawk style",
    "Ponytail": "Hair pulled back in ponytail, high or low positioning",
    "Two-Toned": "Hair with highlights, lowlights, or ombre coloring",
    "Natural Gray": "Natural gray or silver hair, distinguished and elegant"
}