import google.generativeai as genai

# Test the API key
api_key = "AQ.Ab8RN6JXWzvDcBt5vuin71G0kKcRLpv2Zg1oMP5qrCTM0u3Wgw"

print("Testing Google Gemini API key...")
print(f"API Key: {api_key[:20]}...")
print("-" * 50)

try:
    # Configure the API
    genai.configure(api_key=api_key)
    
    # List available models to test connection
    print("Attempting to list available models...")
    models = genai.list_models()
    
    print("✅ API Key is valid! Available models:")
    for model in models:
        if 'gemini' in model.name.lower():
            print(f"  - {model.name}")
    
    # Try a simple text generation
    print("\n" + "-" * 50)
    print("Testing text generation with Gemini Pro...")
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say 'API test successful' if you can read this.")
    
    print(f"Response: {response.text}")
    print("\n✅ API is fully functional!")
    
except Exception as e:
    print(f"❌ API Error: {str(e)}")
    print("\nPossible issues:")
    print("1. Invalid API key")
    print("2. API key doesn't have required permissions")
    print("3. Network connectivity issues")
    print("4. API quota exceeded")
    
    # Check if it's an authentication error
    if "api_key" in str(e).lower() or "invalid" in str(e).lower():
        print("\n⚠️  This appears to be an invalid API key.")
        print("Please verify you have the correct Google AI Studio API key.")
        print("You can get one at: https://makersuite.google.com/app/apikey")