import os
from openai import OpenAI
from qwen_ai_client import QwenHairTransfer

# Test the Qwen API key
api_key = "sk-f4e51b7452dc4d3ca3e8a8d48bfd4884"

print("Testing Qwen API key...")
print(f"API Key: {api_key[:20]}...")
print("-" * 50)

try:
    # Test basic API connection using OpenAI client
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    )
    
    print("Testing basic API connection...")
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {
                "role": "user", 
                "content": "Say 'API test successful' if you can read this."
            }
        ],
        max_tokens=50
    )
    
    print("✅ API Key is valid!")
    print(f"Response: {completion.choices[0].message.content}")
    
    # Test the hair transfer client
    print("\n" + "-" * 50)
    print("Testing QwenHairTransfer client...")
    
    hair_client = QwenHairTransfer()
    print("✅ QwenHairTransfer client initialized successfully!")
    print("\n✅ API is fully functional!")
        
except Exception as e:
    print(f"❌ API Error: {str(e)}")
    print("\nPossible issues:")
    print("1. Invalid API key")
    print("2. API endpoint not available")
    print("3. Network connectivity issues")
    print("4. API quota exceeded")
    
    # Check if it's an authentication error
    if "unauthorized" in str(e).lower() or "invalid" in str(e).lower():
        print("\n⚠️  This appears to be an invalid API key.")
        print("Please verify you have the correct Qwen API key.")