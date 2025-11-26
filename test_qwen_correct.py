import json
import os
try:
    import dashscope
    from dashscope import MultiModalConversation
    print("✅ dashscope library found")
except ImportError:
    print("❌ dashscope library not found, installing...")
    os.system("pip install dashscope")
    import dashscope
    from dashscope import MultiModalConversation

# Configure API
API_KEY = "sk-f4e51b7452dc4d3ca3e8a8d48bfd4884"
dashscope.api_key = API_KEY
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

print("🔄 Testing Qwen Image Edit Plus with dashscope library...")
print("-" * 50)

# Create and save test image
from PIL import Image, ImageDraw
test_image = Image.new('RGB', (512, 512), color='white')
draw = ImageDraw.Draw(test_image)
draw.ellipse([150, 150, 350, 350], outline='black', width=3)  # Face
draw.ellipse([200, 200, 220, 220], outline='black', width=2)  # Left eye  
draw.ellipse([280, 200, 300, 220], outline='black', width=2)  # Right eye
draw.arc([200, 250, 300, 300], 0, 180, fill='black', width=2)  # Smile
test_image.save("test_face_for_api.png")
print("📸 Test image saved as test_face_for_api.png")

# Test 1: Using local file path
print("\n1️⃣ Testing with local image file...")

try:
    response = MultiModalConversation.call(
        model='qwen-image-edit-plus',
        messages=[
            {
                "role": "user",
                "content": [
                    {"text": "Give this person long blonde wavy hair"},
                    {"image": "file://test_face_for_api.png"}
                ]
            }
        ]
    )
    
    if response.status_code == 200:
        print("✅ Success! Response:")
        print(json.dumps(response.output, indent=2, ensure_ascii=False))
        
        # Check for generated image
        if 'choices' in response.output and response.output['choices']:
            choice = response.output['choices'][0]
            if 'message' in choice and 'content' in choice['message']:
                content = choice['message']['content']
                if isinstance(content, list):
                    for item in content:
                        if 'image' in item:
                            print(f"🎨 Generated image: {item['image'][:100]}...")
    else:
        print(f"❌ Error: {response}")
        
except Exception as e:
    print(f"❌ Exception: {str(e)}")

# Test 2: Try different message format
print("\n2️⃣ Testing alternative message format...")

try:
    response = MultiModalConversation.call(
        model='qwen-image-edit',  # Try base model
        messages=[
            {
                "role": "user", 
                "content": [
                    {"text": "Transform this person's hairstyle to have long wavy blonde hair"},
                    {"image": "test_face_for_api.png"}  # Without file:// prefix
                ]
            }
        ]
    )
    
    if response.status_code == 200:
        print("✅ Success! Response:")
        print(json.dumps(response.output, indent=2, ensure_ascii=False))
    else:
        print(f"❌ Error: {response}")
        
except Exception as e:
    print(f"❌ Exception: {str(e)}")

# Test 3: Try absolute path
print("\n3️⃣ Testing with absolute path...")

import os
abs_path = os.path.abspath("test_face_for_api.png")
print(f"Absolute path: {abs_path}")

try:
    response = MultiModalConversation.call(
        model='qwen-image-edit-plus',
        messages=[
            {
                "role": "user",
                "content": [
                    {"text": "Give this person long blonde wavy hair. Keep everything else the same."},
                    {"image": abs_path}
                ]
            }
        ]
    )
    
    if response.status_code == 200:
        print("✅ Success! Response:")
        print(json.dumps(response.output, indent=2, ensure_ascii=False))
    else:
        print(f"❌ Error: {response}")
        
except Exception as e:
    print(f"❌ Exception: {str(e)}")

print("\n" + "=" * 50)
print("Test complete!")