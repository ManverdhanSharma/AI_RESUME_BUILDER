import google.generativeai as genai
import os
import time

# Method 1: Try loading from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"✅ Loaded from .env: {'Yes' if api_key else 'No'}")
except:
    api_key = None
    print("❌ Could not load from .env")

# Method 2: Set directly if .env failed
if not api_key:
    api_key = "AIzaSyBPRo9P3iom7ilrNFt59Rd7RFklOzw5TVQ"  # Your actual API key
    os.environ["GEMINI_API_KEY"] = api_key
    print("✅ Set API key directly")

# Configure Gemini
if api_key:
    genai.configure(api_key=api_key)
    print("✅ Gemini API configured")
else:
    print("❌ No API key available")

def enhance_content(content: str, content_type: str) -> str:
    """
    Enhance resume content using Google Gemini AI
    """
    
    print(f"\n🔧 DEBUG: enhance_content called")
    print(f"Content type: {content_type}")
    print(f"Original content: '{content}'")
    
    # Check API key again
    current_key = os.getenv("GEMINI_API_KEY")
    if not current_key:
        print("❌ No API key found - returning original content")
        return content
    else:
        print("✅ API key found, proceeding with enhancement")
    
    try:
        print("🤖 Initializing Gemini model...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Improve this text by fixing spelling errors and making it more professional: {content}"
        
        print("📝 Sending request to AI...")
        response = model.generate_content(prompt)
        
        if response and hasattr(response, 'text') and response.text:
            enhanced_text = response.text.strip()
            print(f"✅ AI Response received: '{enhanced_text[:50]}...'")
            return enhanced_text
        else:
            print("❌ No valid response from AI")
            return content
            
    except Exception as e:
        print(f"❌ AI enhancement failed: {e}")
        return content

# Test function
def quick_test():
    test_text = "I have experiance in Python programming"
    result = enhance_content(test_text, "professional_summary")
    print(f"\nQuick Test Result:")
    print(f"Original: {test_text}")
    print(f"Enhanced: {result}")
    print(f"Changed: {'✅ Yes' if result != test_text else '❌ No'}")

if __name__ == "__main__":
    quick_test()
