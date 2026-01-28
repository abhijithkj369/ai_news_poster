import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

class AIProcessor:
    def __init__(self, api_key):
        # 1. Try the newest model from your debug list (often has fresh quota)
        self.model_name = "gemini-2.5-flash" 
        print(f"🔧 AI Processor initialized with model: {self.model_name}")
        
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )

    def shortlist_news(self, news_list):
        """Uses AI to pick the story. Returns a DEFAULT if AI fails (Graceful Fallback)."""
        try:
            print("🧠 Asking AI to shortlist news...")
            titles = "\n".join([f"- {n['title']}" for n in news_list])
            
            prompt = f"""
            Pick the SINGLE best AI news headline for LinkedIn:
            {titles}
            Return ONLY the title.
            """
            response = self.llm.invoke(prompt)
            return response.content.strip()

        except Exception as e:
            # THIS IS THE FIX: If API blocks us, we use a fallback so the project continues!
            print(f"⚠️ API Limit Hit ({e}). Switching to FALLBACK mode.")
            print("   (Using the first scraped story to ensure Image Gen works)")
            if news_list:
                return news_list[0]['title']
            return "The Future of Artificial Intelligence in 2026"

    def extract_style_from_image(self, image_path):
        """Vision analysis. Returns DEFAULT style if AI fails."""
        try:
            print(f"👀 Analyzing image style with {self.model_name}...")
            message = HumanMessage(
                content=[
                    {"type": "text", "text": "Describe the artistic style of this image for a prompt."},
                    {"type": "image_url", "image_url": image_path}
                ]
            )
            response = self.llm.invoke([message])
            return response.content.strip()
            
        except Exception as e:
            print(f"⚠️ Vision API Warning: {e}")
            print("   (Using DEFAULT style to proceed to generation)")
            return "Futuristic, high-tech, minimal, 3d render, isometric, cinematic lighting, professional 8k"