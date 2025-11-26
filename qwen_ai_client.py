import os
import requests
import json
import io
import base64
from typing import Optional, Dict, Any, List
from PIL import Image
import uuid
import dashscope
from dashscope import MultiModalConversation

class QwenHairTransfer:
    """
    Client for Qwen API to perform hair style transformation and generation
    using Qwen Image Edit Plus model for actual image generation
    """
    
    def __init__(self, api_key=None):
        # Configure Qwen with dashscope
        self.api_key = api_key or os.getenv("QWEN_API_KEY", "sk-f4e51b7452dc4d3ca3e8a8d48bfd4884")
        dashscope.api_key = self.api_key
        dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
        self.model = "qwen-image-edit-plus-2025-10-30"
        
    def load_image(self, image_path: str) -> Image.Image:
        """Load image from file path"""
        return Image.open(image_path)
    
    def image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')
    
    def hair_transfer(self, 
                     user_image_path: str, 
                     hairstyle_image_path: Optional[str] = None,
                     prompt_override: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform hair style transformation using Qwen Image Edit Plus
        
        Args:
            user_image_path: Path to the user's photo
            hairstyle_image_path: Optional path to reference hairstyle (can be None)
            prompt_override: Text description of desired hairstyle transformation
            
        Returns:
            API response with the generated images
        """
        
        try:
            # Analyze hairstyle first if reference image is provided
            hairstyle_description = ""
            if hairstyle_image_path:
                print("🔍 Analyzing reference hairstyle...")
                hairstyle_description = self.analyze_hairstyle(hairstyle_image_path)
                
                # Check if analysis was successful
                if "cannot analyze" in hairstyle_description.lower() or "sorry" in hairstyle_description.lower() or len(hairstyle_description) < 50:
                    print("⚠️ Vision analysis failed, using fallback description")
                    hairstyle_description = "the hairstyle shown in the reference image with all its specific characteristics including cut, color, length, texture, and styling"
                else:
                    print(f"📋 Analysis complete: {hairstyle_description[:100]}...")
            
            # Create a descriptive prompt based on whether we have reference image
            if hairstyle_image_path:
                # Two-image mode: user + reference with detailed analysis
                if prompt_override:
                    enhanced_prompt = f"HAIR TRANSFER TASK: Apply this hairstyle to the person: {hairstyle_description}. {prompt_override}"
                else:
                    enhanced_prompt = f"Transform the person's hair to match this exact hairstyle: {hairstyle_description}. Keep the person's face, skin, clothing, and background unchanged. Only change the hair to precisely match the described style."
            else:
                # Single-image mode: user + text description
                if prompt_override:
                    enhanced_prompt = prompt_override
                else:
                    enhanced_prompt = "Transform this person's hairstyle. Keep all facial features, skin tone, clothing, and background exactly the same. Only change the hair naturally and realistically."
            
            # Hybrid approach: Use detailed analysis + visual reference
            if hairstyle_image_path:
                # Two-image mode: Analysis-guided hair transfer
                content = [
                    {"text": "Hair Transformation Task:"},
                    {"text": f"DETAILED HAIRSTYLE SPECIFICATIONS: {hairstyle_description}"},
                    {"text": "Reference image:"},
                    {"image": hairstyle_image_path},
                    {"text": "Person to transform:"},
                    {"image": user_image_path},
                    {"text": enhanced_prompt}
                ]
            else:
                # Single-image mode
                content = [{"text": enhanced_prompt}, {"image": user_image_path}]
            
            # Use dashscope MultiModalConversation for actual image generation
            response = MultiModalConversation.call(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )
            
            if response.status_code == 200 and response.output:
                # Extract generated images from response
                generated_images = []
                
                if 'choices' in response.output and response.output['choices']:
                    choice = response.output['choices'][0]
                    if 'message' in choice and 'content' in choice['message']:
                        content = choice['message']['content']
                        if isinstance(content, list):
                            for item in content:
                                if 'image' in item and item['image']:
                                    # Download the generated image
                                    img_url = item['image']
                                    try:
                                        img_response = requests.get(img_url)
                                        if img_response.status_code == 200:
                                            # Save image locally
                                            output_path = f"outputs/generated_hair_{uuid.uuid4().hex[:8]}.png"
                                            os.makedirs("outputs", exist_ok=True)
                                            
                                            with open(output_path, 'wb') as f:
                                                f.write(img_response.content)
                                            
                                            generated_images.append(output_path)
                                    except Exception as e:
                                        print(f"Error downloading image: {e}")
                
                if generated_images:
                    return {
                        "status": "success",
                        "generated_images": generated_images,
                        "description": f"Successfully generated {len(generated_images)} hair style transformation(s)",
                        "raw_response": response.output
                    }
                else:
                    return {
                        "error": "No images generated in response",
                        "status": "failed",
                        "raw_response": response.output
                    }
            else:
                return {
                    "error": f"API call failed: {response}",
                    "status": "failed"
                }
                
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def analyze_hairstyle(self, hairstyle_image_path: str) -> str:
        """
        Analyze a hairstyle image in detail using Qwen vision model
        
        Args:
            hairstyle_image_path: Path to the hairstyle reference image
            
        Returns:
            Detailed description of the hairstyle
        """
        try:
            # Use Qwen vision model to analyze the hairstyle in detail
            response = MultiModalConversation.call(
                model="qwen-vl-max",  # Use vision model for analysis
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"text": """Analyze this hairstyle image in extreme detail. Describe EVERY aspect of the hair:

1. HAIR LENGTH: Specific length (very short, short, medium, long, very long)
2. HAIR CUT STYLE: Type of cut (bob, pixie, layered, blunt, etc.)
3. HAIR COLOR: Exact colors, highlights, lowlights, ombre, balayage
4. HAIR TEXTURE: Straight, wavy, curly, coily, fine, thick
5. HAIR STYLING: How it's styled (sleek, tousled, voluminous, flat)
6. PARTING: Side part, middle part, no part, deep part
7. LAYERS: Number and type of layers (face-framing, long layers, short layers)
8. BANGS/FRINGE: Type and style if present
9. VOLUME: Where the volume is concentrated
10. SPECIAL FEATURES: Any unique characteristics

Provide a comprehensive, detailed description that would allow someone to recreate this exact hairstyle."""},
                            {"image": hairstyle_image_path}
                        ]
                    }
                ]
            )
            
            if response.status_code == 200 and response.output:
                if 'choices' in response.output and response.output['choices']:
                    choice = response.output['choices'][0]
                    if 'message' in choice and 'content' in choice['message']:
                        content = choice['message']['content']
                        if isinstance(content, list):
                            # Extract text from content
                            for item in content:
                                if 'text' in item:
                                    return item['text']
                        elif isinstance(content, str):
                            return content
            
            return "Unable to analyze hairstyle details"
            
        except Exception as e:
            print(f"Error analyzing hairstyle: {e}")
            return f"Analysis error: {str(e)}"
    
    def generate_transformation_guide(self, result: Dict[str, Any]) -> str:
        """
        Extract transformation guide from the result
        
        Args:
            result: API response containing the analysis
            
        Returns:
            Formatted transformation guide
        """
        if result.get("status") == "success" and "description" in result:
            return result["description"]
        return "Unable to generate transformation guide"