import google.generativeai as genai
from PIL import Image
import io
from typing import Optional, Dict, Any, List
import json

class HairStylingAdvisor:
    """
    AI-powered hair styling advisor that provides recommendations
    without generating transformed images
    """
    
    def __init__(self):
        self.api_key = "AIzaSyCQQ8-NGgeequPtR9FsMnU0SNAbg6LFiYw"
        genai.configure(api_key=self.api_key)
        
        # Use standard Gemini model for analysis
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    def load_image(self, image_path: str) -> Image.Image:
        """Load image from file path"""
        return Image.open(image_path)
    
    def analyze_face_and_recommend(self, 
                                   user_image_path: str,
                                   desired_style: str,
                                   preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze user's face and provide styling recommendations
        """
        try:
            user_image = self.load_image(user_image_path)
            
            prompt = f"""
            You are a professional hair styling consultant. Analyze this photo and provide detailed styling recommendations.
            
            The client is interested in: {desired_style}
            
            Additional preferences: {json.dumps(preferences) if preferences else 'None specified'}
            
            Please provide:
            
            1. FACE SHAPE ANALYSIS:
            - Identified face shape
            - Key facial features to consider
            
            2. STYLE COMPATIBILITY (Rate 1-10):
            - How well the requested style would suit them
            - Specific reasons why
            
            3. RECOMMENDED ADJUSTMENTS:
            - How to adapt the style for their features
            - Specific modifications needed
            
            4. STYLING TIPS:
            - How to achieve this look
            - Products needed
            - Daily maintenance required
            
            5. ALTERNATIVE SUGGESTIONS:
            - 3 other styles that would suit them well
            - Why these alternatives work
            
            6. COLOR RECOMMENDATIONS:
            - Best hair colors for their skin tone
            - If they want highlights/lowlights suggestions
            
            7. PROFESSIONAL NOTES:
            - What to tell their hairstylist
            - Reference points for the salon
            
            Format the response in clear sections with emojis for visual appeal.
            Be encouraging and professional in tone.
            """
            
            response = self.model.generate_content([prompt, user_image])
            
            return {
                "status": "success",
                "analysis": response.text,
                "style_requested": desired_style
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def compare_styles(self, 
                      user_image_path: str,
                      style_options: List[str]) -> Dict[str, Any]:
        """
        Compare multiple style options for the user
        """
        try:
            user_image = self.load_image(user_image_path)
            
            styles_text = "\n".join([f"{i+1}. {style}" for i, style in enumerate(style_options)])
            
            prompt = f"""
            As a professional hair styling consultant, compare these hairstyle options for this client:
            
            {styles_text}
            
            For each style, provide:
            - Compatibility score (1-10)
            - Key advantages
            - Potential challenges
            - Maintenance level
            
            Then recommend the TOP choice with detailed reasoning.
            
            Format with clear headers and use emojis for visual appeal.
            """
            
            response = self.model.generate_content([prompt, user_image])
            
            return {
                "status": "success",
                "comparison": response.text,
                "styles_compared": style_options
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def virtual_consultation(self, 
                            user_image_path: str,
                            consultation_type: str = "general") -> Dict[str, Any]:
        """
        Provide a complete virtual consultation
        """
        try:
            user_image = self.load_image(user_image_path)
            
            consultation_prompts = {
                "general": """
                Provide a comprehensive hair consultation including:
                - Current hair analysis
                - Face shape and features
                - Top 5 recommended styles
                - Color suggestions
                - Maintenance tips
                - Products recommendations
                """,
                "makeover": """
                Suggest a complete hair makeover:
                - Dramatic style changes that would work
                - Bold color options
                - Modern trending styles suitable for them
                - Step-by-step transformation plan
                - Expected results and timeline
                """,
                "professional": """
                Recommend professional/office-appropriate styles:
                - Conservative yet stylish options
                - Easy morning routine styles
                - Low-maintenance professional looks
                - Polish and sophistication factors
                """,
                "special_event": """
                Suggest special event hairstyles:
                - Formal occasion styles
                - Wedding guest options
                - Party looks
                - How to request these at a salon
                """
            }
            
            prompt = f"""
            You are an expert hair stylist providing a virtual consultation.
            
            {consultation_prompts.get(consultation_type, consultation_prompts['general'])}
            
            Be specific, encouraging, and professional.
            Use emojis to make the response engaging.
            Format with clear sections and bullet points.
            """
            
            response = self.model.generate_content([prompt, user_image])
            
            return {
                "status": "success",
                "consultation": response.text,
                "type": consultation_type
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

# Hair style categories for recommendations
STYLE_CATEGORIES = {
    "Classic": [
        "Classic Bob",
        "Sleek Straight",
        "Soft Waves",
        "Side Part",
        "Low Bun"
    ],
    "Modern": [
        "Textured Lob",
        "Shag Cut",
        "Curtain Bangs",
        "Wolf Cut",
        "Butterfly Cut"
    ],
    "Edgy": [
        "Pixie Cut",
        "Undercut",
        "Asymmetric Bob",
        "Mohawk Style",
        "Buzz Cut"
    ],
    "Romantic": [
        "Beach Waves",
        "Loose Curls",
        "Braided Crown",
        "Soft Layers",
        "Hollywood Waves"
    ],
    "Professional": [
        "Sleek Low Ponytail",
        "French Twist",
        "Polished Bob",
        "Neat Bun",
        "Shoulder-Length Layers"
    ],
    "Natural": [
        "Afro",
        "Natural Curls",
        "Protective Styles",
        "Locs",
        "Twist Out"
    ]
}