import os
import base64
import mimetypes
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from config import settings  # <--- IMPORT YOUR SETTINGS

class AIProcessor:
    def __init__(self):
        self.model_name = settings.AI_MODEL_NAME
        print(f"🔧 AI Processor initialized with model: {self.model_name}")
        
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7,
            convert_system_message_to_human=True
        )

    def shortlist_news(self, news_list):
        try:
            print("🧠 Asking AI to shortlist news...")
            titles = "\n".join([f"- {n['title']}" for n in news_list])
            prompt = f"Pick the SINGLE best AI news headline for LinkedIn:\n{titles}\nReturn ONLY the title."
            response = self.llm.invoke(prompt)
            return response.content.strip()
        except Exception as e:
            print(f"⚠️ Shortlist Error: {e}. Using fallback.")
            return news_list[0]['title'] if news_list else "AI News of the Day"

    def extract_style_from_image(self, image_path):
        try:
            print(f"👀 Analyzing image style with {self.model_name}...")
            
            # --- THE FIX: Convert Image to Base64 ---
            # 1. Detect file type (jpg, png, etc.)
            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type: mime_type = "image/jpeg"
            
            # 2. Read and Encode
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            
            # 3. Create Data URI (The format the API wants)
            image_data_url = f"data:{mime_type};base64,{encoded_string}"
            
            message = HumanMessage(
                content=[
                    {"type": "text", "text": "Describe the artistic style, lighting, and composition of this image. Provide a detailed prompt fragment that can be used to generate a new image in this exact style. Do not describe the subject, only the aesthetic."},
                    {"type": "image_url", "image_url": image_data_url}
                ]
            )
            response = self.llm.invoke([message])
            return response.content.strip()
            
        except Exception as e:
            print(f"⚠️ Vision Error: {e}")
            return "Futuristic, high-tech, minimal, 3d render, isometric, cinematic lighting, professional 8k"