import requests
import json
import base64
from PIL import Image
import io
import os

# API configuration
API_KEY = "sk-f4e51b7452dc4d3ca3e8a8d48bfd4884"

print("🔄 Testing Qwen Image Edit Plus API for image generation...")
print("-" * 50)

# Create a test image
test_image = Image.new('RGB', (512, 512), color='white')
from PIL import ImageDraw
draw = ImageDraw.Draw(test_image)
draw.ellipse([150, 150, 350, 350], outline='black', width=3)  # Face
draw.ellipse([200, 200, 220, 220], outline='black', width=2)  # Left eye  
draw.ellipse([280, 200, 300, 220], outline='black', width=2)  # Right eye
draw.arc([200, 250, 300, 300], 0, 180, fill='black', width=2)  # Smile
test_image.save("test_face.png")

# Convert to base64
buffer = io.BytesIO()
test_image.save(buffer, format='PNG')
img_bytes = buffer.getvalue()
img_base64 = base64.b64encode(img_bytes).decode('utf-8')

# Test 1: DashScope API format with proper headers
print("\n1️⃣ Testing DashScope API format for image generation...")

url = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "X-DashScope-Async": "enable"  # Try async mode
}

payload = {
    "model": "qwen-image-edit-plus",
    "input": {
        "prompt": "Give this person long blonde wavy hair",
        "image": img_base64  # Try without data:image prefix
    },
    "parameters": {}
}

response = requests.post(url, headers=headers, json=payload)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("✅ Success! Response:")
    print(json.dumps(result, indent=2)[:1000])
else:
    print(f"❌ Error: {response.text[:500]}")

# Test 2: Try with URL format
print("\n2️⃣ Testing with image URL instead of base64...")

# Save image to a temporary location
test_image_path = "test_image_for_api.png"
test_image.save(test_image_path)

# You would normally upload this to a public URL
# For testing, let's try with the base64 in URL format
payload2 = {
    "model": "qwen-image-edit-plus",
    "input": {
        "prompt": "Give this person long blonde wavy hair",
        "image_url": f"data:image/png;base64,{img_base64}"
    },
    "parameters": {}
}

response = requests.post(url, headers=headers, json=payload2)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("✅ Success! Response:")
    print(json.dumps(result, indent=2)[:1000])
else:
    print(f"❌ Error: {response.text[:500]}")

# Test 3: Try multi-modal conversation endpoint
print("\n3️⃣ Testing MultiModal Conversation endpoint...")

conv_url = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
conv_payload = {
    "model": "qwen-image-edit",  # Try the basic model
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": "Give this person long blonde wavy hair"},
                    {"image": img_base64}
                ]
            }
        ]
    }
}

response = requests.post(conv_url, headers=headers, json=conv_payload)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("✅ Success! Response:")
    print(json.dumps(result, indent=2)[:1000])
    
    # Check if there's an output image
    if 'output' in result:
        if 'image' in result['output']:
            print(f"Generated image: {result['output']['image'][:100]}...")
        elif 'url' in result['output']:
            print(f"Generated image URL: {result['output']['url']}")
else:
    print(f"❌ Error: {response.text[:500]}")

print("\n" + "=" * 50)
print("Test complete!")