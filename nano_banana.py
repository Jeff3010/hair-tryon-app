import requests
import base64
import json
from typing import Optional, Dict, Any

class NanoBanana:
    """
    Client for Nano Banana API to perform hair style transfer
    using Gemini 2.5 Flash Image model
    """
    
    def __init__(self):
        # Hardcoded API key as requested
        self.api_key = "AQ.Ab8RN6JXWzvDcBt5vuin71G0kKcRLpv2Zg1oMP5qrCTM0u3Wgw"
        # Try different possible API endpoints
        self.base_url = "https://api.nanobananas.com/v1"  # Added 's' to match common pattern
        self.model = "gemini-2.5-flash-image"
        
    def encode_image_to_base64(self, image_path: str) -> str:
        """Convert image file to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def hair_transfer(self, 
                     user_image_path: str, 
                     hairstyle_image_path: str,
                     prompt_override: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform hair style transfer from reference image to user photo
        
        Args:
            user_image_path: Path to the user's photo
            hairstyle_image_path: Path to the reference hairstyle photo
            prompt_override: Optional custom prompt (if not provided, uses optimized default)
            
        Returns:
            API response with the processed image
        """
        
        # Encode images to base64
        user_image_b64 = self.encode_image_to_base64(user_image_path)
        hairstyle_image_b64 = self.encode_image_to_base64(hairstyle_image_path)
        
        # Highly detailed prompt for accurate hair transfer while preserving facial features
        default_prompt = """
        Task: Virtual Hair Try-On with Precise Feature Preservation
        
        PRIMARY OBJECTIVE: Transfer ONLY the hairstyle from Image 2 to the person in Image 1.
        
        CRITICAL PRESERVATION REQUIREMENTS (DO NOT ALTER):
        1. Facial Features - MUST remain 100% identical:
           - Exact same face shape and bone structure
           - Original eye shape, size, color, and position
           - Original nose shape and size
           - Original mouth and lips exactly as they are
           - Original skin tone and texture
           - All facial marks, moles, or distinguishing features
           - Original facial expressions
        
        2. Physical Attributes to PRESERVE:
           - Body position and pose
           - Clothing and accessories
           - Background environment
           - Image quality and lighting on the face
           - Person's age appearance
           - Gender presentation
           - Ethnic features
        
        HAIR TRANSFER REQUIREMENTS (FROM IMAGE 2):
        1. Hair Style Elements to Transfer:
           - Overall hair shape and volume
           - Hair length (short/medium/long)
           - Hair texture (straight/wavy/curly/kinky)
           - Hair parting style and position
           - Bangs or fringe style if present
           - Hair flow direction and movement
        
        2. Hair Color Adaptation:
           - Transfer the hairstyle SHAPE but adapt the color naturally
           - If the reference has an unnatural color (blue, pink, etc.), adapt it to look realistic on the person
           - Ensure the hair color looks natural with the person's skin tone
        
        3. Natural Integration:
           - Hair should look like it naturally grows from the person's scalp
           - Hairline should match the person's natural hairline
           - Hair should cast appropriate shadows on face and shoulders
           - Hair edges should blend seamlessly, no harsh cutouts
        
        QUALITY REQUIREMENTS:
        - Output must be photorealistic
        - No artifacts or distortions on the face
        - Natural lighting consistency between hair and face
        - Professional photography quality
        
        Image 1 (User Photo): The person whose appearance must be preserved
        Image 2 (Hairstyle Reference): Source for the hairstyle only
        
        Generate a single, high-quality image showing the person from Image 1 with the hairstyle from Image 2, 
        maintaining absolute fidelity to the person's facial features and identity.
        """
        
        prompt = prompt_override if prompt_override else default_prompt
        
        # Prepare API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image",
                            "image": {
                                "base64": user_image_b64
                            }
                        },
                        {
                            "type": "image", 
                            "image": {
                                "base64": hairstyle_image_b64
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.3,  # Lower temperature for more consistent results
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    def save_result_image(self, result: Dict[str, Any], output_path: str):
        """
        Extract and save the generated image from API response
        
        Args:
            result: API response containing the generated image
            output_path: Path where to save the output image
        """
        try:
            # Extract base64 image from response (adjust based on actual API response format)
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0].get("message", {}).get("content", "")
                
                # If content contains base64 image data
                if isinstance(content, str) and content.startswith("data:image"):
                    # Remove data URL prefix
                    base64_data = content.split(",")[1]
                    image_data = base64.b64decode(base64_data)
                    
                    with open(output_path, "wb") as f:
                        f.write(image_data)
                    return True
                    
            return False
        except Exception as e:
            print(f"Error saving image: {e}")
            return False