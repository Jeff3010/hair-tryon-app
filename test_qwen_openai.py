from openai import OpenAI
import base64
from PIL import Image
import io

# API configuration
API_KEY = "sk-f4e51b7452dc4d3ca3e8a8d48bfd4884"

# Create OpenAI client with Qwen endpoint
client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

print("🔄 Testing Qwen API with OpenAI-compatible format...")
print("-" * 50)

# Create a simple test image
test_image = Image.new('RGB', (512, 512), color='white')
from PIL import ImageDraw
draw = ImageDraw.Draw(test_image)
draw.ellipse([150, 150, 350, 350], outline='black', width=3)  # Face
draw.ellipse([200, 200, 220, 220], outline='black', width=2)  # Left eye  
draw.ellipse([280, 200, 300, 220], outline='black', width=2)  # Right eye
draw.arc([200, 250, 300, 300], 0, 180, fill='black', width=2)  # Smile

# Convert to base64
buffer = io.BytesIO()
test_image.save(buffer, format='PNG')
img_bytes = buffer.getvalue()
img_base64 = base64.b64encode(img_bytes).decode('utf-8')

# Test with vision model
try:
    print("Testing qwen-vl-plus model...")
    completion = client.chat.completions.create(
        model="qwen-vl-plus",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe what you see in this image. Is there a face?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    
    print("✅ Success! Response:")
    print(completion.choices[0].message.content)
    
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "-" * 50)

# Test with a real image file if available
import os
if os.path.exists("uploads/user_IMG_3178.jpg"):
    print("\n📸 Testing with real uploaded image...")
    
    with open("uploads/user_IMG_3178.jpg", "rb") as f:
        real_img_bytes = f.read()
        real_img_base64 = base64.b64encode(real_img_bytes).decode('utf-8')
    
    try:
        completion = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe the person's current hairstyle in this photo."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{real_img_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        print("✅ Success with real image!")
        print(completion.choices[0].message.content)
        
    except Exception as e:
        print(f"❌ Error with real image: {str(e)}")
else:
    print("\nℹ️ No real uploaded images found in uploads/ directory")

print("\n" + "=" * 50)
print("Test complete!")