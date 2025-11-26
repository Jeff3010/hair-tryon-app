import requests
import json

# Test the Nano Banana API access
api_key = "AQ.Ab8RN6JXWzvDcBt5vuin71G0kKcRLpv2Zg1oMP5qrCTM0u3Wgw"

# Try different possible endpoints
endpoints = [
    "https://api.nanobanana.com/v1",
    "https://api.nanobananas.com/v1", 
    "https://api.nano-banana.com/v1",
    "https://api.nanobanana.ai/v1",
    "https://nanobanana.ai/api/v1",
    "https://api.nanobanana.io/v1"
]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Simple test payload
test_payload = {
    "model": "gemini-2.5-flash-image",
    "messages": [
        {
            "role": "user",
            "content": "Hello, testing API connection"
        }
    ],
    "max_tokens": 10
}

print("Testing Nano Banana API endpoints...")
print(f"Using API key: {api_key[:20]}...")
print("-" * 50)

for endpoint in endpoints:
    print(f"\nTrying: {endpoint}/chat/completions")
    try:
        response = requests.post(
            f"{endpoint}/chat/completions",
            headers=headers,
            json=test_payload,
            timeout=5,
            verify=True
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ SUCCESS! This endpoint works.")
            print(f"Response: {response.json()}")
            break
        else:
            print(f"Response: {response.text[:200]}")
    except requests.exceptions.SSLError as e:
        print(f"❌ SSL Error: {str(e)[:100]}")
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {str(e)[:100]}")
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Error: {str(e)[:100]}")

print("\n" + "-" * 50)
print("If none of the endpoints work, please check:")
print("1. The API key is correct")
print("2. The correct Nano Banana API endpoint URL")
print("3. Your internet connection")
print("4. If the service requires special headers or authentication format")