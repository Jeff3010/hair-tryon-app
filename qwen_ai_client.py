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
            # Create a descriptive prompt based on whether we have reference image
            if hairstyle_image_path:
                # Two-image mode: user + reference - VERY explicit about hair transfer
                if prompt_override:
                    enhanced_prompt = f"HAIR TRANSFER TASK: Take the hairstyle from the second image and put it on the person in the first image. {prompt_override}"
                else:
                    enhanced_prompt = """DETAILED HAIR TRANSPLANT OPERATION:

🔍 ANALYSIS PHASE:
1. Examine the TARGET HAIRSTYLE image in extreme detail
2. Note EVERY hair characteristic: cut pattern, layers, length variations, color tones, highlights, texture, volume, styling direction, parting, bangs/fringe, etc.

✂️ TRANSFER PHASE:
1. Remove ALL existing hair from the SOURCE PERSON
2. Apply the TARGET HAIRSTYLE with 100% accuracy
3. Match hair color EXACTLY (including highlights/lowlights)
4. Replicate the exact cut, layers, and styling
5. Maintain the same hair volume and texture as shown in target
6. Copy the parting style and direction precisely

🎯 QUALITY CONTROL:
- The result must be indistinguishable from the SOURCE PERSON having naturally grown the TARGET HAIRSTYLE
- Hair must look realistic and natural on the person's head shape
- Preserve face, skin, clothing, background unchanged
- Final image should show perfect hair transfer with zero compromise on accuracy"""
            else:
                # Single-image mode: user + text description
                if prompt_override:
                    enhanced_prompt = prompt_override
                else:
                    enhanced_prompt = "Transform this person's hairstyle. Keep all facial features, skin tone, clothing, and background exactly the same. Only change the hair naturally and realistically."
            
            # Prepare content with enhanced image labeling for better recognition
            if hairstyle_image_path:
                # Two-image mode: Very explicit labeling with role definitions
                content = [
                    {"text": "🎯 HAIR TRANSFER MISSION:"},
                    {"text": "📸 SOURCE PERSON (to be transformed):"},
                    {"image": user_image_path},
                    {"text": "✂️ TARGET HAIRSTYLE (to copy exactly):"},
                    {"image": hairstyle_image_path},
                    {"text": enhanced_prompt},
                    {"text": "⚠️ CRITICAL: Analyze the TARGET HAIRSTYLE image in detail and replicate EVERY aspect (cut, length, layers, color, texture, styling) onto the SOURCE PERSON. The result must show the SOURCE PERSON with the EXACT hairstyle from the TARGET image."}
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