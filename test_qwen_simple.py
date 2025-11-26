import requests
import base64
import json
from PIL import Image
import io

# API configuration
API_KEY = "sk-f4e51b7452dc4d3ca3e8a8d48bfd4884"
API_URL = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
MODEL = "qwen-image-edit-plus"

# Create a simple test image (white square)
test_image = Image.new('RGB', (512, 512), color='white')

# Add a simple face drawing (optional - just for testing)
from PIL import ImageDraw
draw = ImageDraw.Draw(test_image)
# Draw a simple face
draw.ellipse([150, 150, 350, 350], outline='black', width=3)  # Face
draw.ellipse([200, 200, 220, 220], outline='black', width=2)  # Left eye
draw.ellipse([280, 200, 300, 220], outline='black', width=2)  # Right eye
draw.arc([200, 250, 300, 300], 0, 180, fill='black', width=2)  # Smile

# Save test image
test_image.save("test_face.png")
print("✅ Test image created: test_face.png")

# Convert image to base64
buffer = io.BytesIO()
test_image.save(buffer, format='PNG')
img_bytes = buffer.getvalue()
img_base64 = base64.b64encode(img_bytes).decode('utf-8')

# Test prompt
prompt = "Give this person long wavy blonde hair"

print("\n🔄 Testing Qwen API...")
print(f"Model: {MODEL}")
print(f"Prompt: {prompt}")
print("-" * 50)

# Prepare API request
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Try different payload formats to find what works
print("\n1️⃣ Testing format 1: Simple image + prompt")
payload1 = {
    "model": MODEL,
    "input": {
        "prompt": prompt,
        "image": f"data:image/png;base64,{img_base64}"
    },
    "parameters": {}
}

response = requests.post(API_URL, headers=headers, json=payload1)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("✅ Success! Response:")
    print(json.dumps(result, indent=2))
else:
    print(f"❌ Error: {response.text[:500]}")

print("\n" + "-" * 50)
print("\n2️⃣ Testing format 2: Image URL field")
payload2 = {
    "model": MODEL,
    "input": {
        "prompt": prompt,
        "image_url": f"data:image/png;base64,{img_base64}"
    },
    "parameters": {}
}

response = requests.post(API_URL, headers=headers, json=payload2)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("✅ Success! Response:")
    print(json.dumps(result, indent=2))
else:
    print(f"❌ Error: {response.text[:500]}")

print("\n" + "-" * 50)
print("\n3️⃣ Testing format 3: Images array")
payload3 = {
    "model": MODEL,
    "input": {
        "prompt": prompt,
        "images": [f"data:image/png;base64,{img_base64}"]
    },
    "parameters": {}
}

response = requests.post(API_URL, headers=headers, json=payload3)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("✅ Success! Response:")
    print(json.dumps(result, indent=2))
else:
    print(f"❌ Error: {response.text[:500]}")

print("\n" + "=" * 50)
print("Test complete!")