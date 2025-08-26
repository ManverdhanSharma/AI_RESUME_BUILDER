import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Test API key
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {'✅ Yes' if api_key else '❌ No'}")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # First, let's see what models are available
        print("\n🔍 Available models:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"  - {m.name}")
        
        # Use the correct model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Simple test
        response = model.generate_content("Fix this spelling: I have experiance in Python programming")
        print(f"\n✅ API Test Successful!")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ API Test Failed: {e}")
else:
    print("❌ Please add your GEMINI_API_KEY to the .env file")
