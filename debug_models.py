import os
from dotenv import load_dotenv
import google.generativeai as genai

def list_available_models():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ No API Key found in .env")
        return

    genai.configure(api_key=api_key)
    
    print(f"🔍 Checking available models for your key...")
    print(f"KEY: {api_key[:5]}...{api_key[-5:]}") # Security check: prints first/last 5 chars
    
    try:
        available_models = []
        for m in genai.list_models():
            # We only care about models that can generate content (text/images)
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ FOUND: {m.name}")
                available_models.append(m.name)
        
        if not available_models:
            print("⚠️ No content generation models found. Check your API Key permissions.")
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")

if __name__ == "__main__":
    list_available_models()