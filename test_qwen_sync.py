import requests
import json
import base64
from PIL import Image
import io

# API configuration
API_KEY = "sk-f4e51b7452dc4d3ca3e8a8d48bfd4884"

print("🔄 Testing Qwen Image Edit Plus API (SYNC mode)...")
print("-" * 50)

# Create a test image
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

# Test 1: Synchronous API call without async header
print("\n1️⃣ Testing synchronous DashScope API...")

url = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    # Removed async header
}

payload = {
    "model": "qwen-image-edit-plus",
    "input": {
        "prompt": "Give this person long blonde wavy hair",
        "image": img_base64
    },
    "parameters": {
        "n": 1  # Generate 1 image
    }
}

response = requests.post(url, headers=headers, json=payload)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("✅ Success! Response:")
    print(json.dumps(result, indent=2)[:1000])
else:
    print(f"❌ Error: {response.text}")

# Test 2: Try different model name
print("\n2️⃣ Testing with qwen-image-edit model...")

payload2 = {
    "model": "qwen-image-edit",  # Use base model instead of plus
    "input": {
        "prompt": "Give this person long blonde wavy hair",
        "image": img_base64
    },
    "parameters": {
        "n": 1
    }
}

response = requests.post(url, headers=headers, json=payload2)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("✅ Success! Response:")
    print(json.dumps(result, indent=2)[:1000])
else:
    print(f"❌ Error: {response.text}")

# Test 3: Try conversation format
print("\n3️⃣ Testing conversation format...")

payload3 = {
    "model": "qwen-image-edit-plus",
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

response = requests.post(url, headers=headers, json=payload3)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("✅ Success! Response:")
    print(json.dumps(result, indent=2)[:1000])
else:
    print(f"❌ Error: {response.text}")

# Test 4: Try with direct image field (no data: prefix)
print("\n4️⃣ Testing with raw base64...")

payload4 = {
    "model": "qwen-image-edit-plus",
    "input": {
        "prompt": "Give this person long blonde wavy hair",
        "image": img_base64  # Raw base64 without data: prefix
    }
}

response = requests.post(url, headers=headers, json=payload4)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

print("\n" + "=" * 50)
print("Test complete!")