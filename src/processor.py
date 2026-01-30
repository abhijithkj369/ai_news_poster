from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from config import settings
import base64

class AIProcessor:
    def __init__(self):
        print(f"🔧 Local AI Processor initialized with: {settings.LLM_MODEL}")
        
        # Connects to your local Ollama server (usually localhost:11434)
        self.llm = ChatOllama(
            model=settings.LLM_MODEL,
            temperature=0.7,
        )

    def shortlist_news(self, news_list):
        print("🧠 Asking Local Llama to shortlist news...")
        titles = "\n".join([f"- {n['title']}" for n in news_list])
        prompt = f"Pick the SINGLE best AI news headline for LinkedIn:\n{titles}\nReturn ONLY the title."
        
        # Llama 3.2 is chat-optimized, so we send a standard string
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def extract_style_from_image(self, image_path):
        print(f"👀 Local Vision Analysis on: {image_path}")
        
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        message = HumanMessage(
            content=[
                # CHANGED: Added "Keep it under 40 words" to fix the Token Limit warning
                {"type": "text", "text": "Describe the artistic style, typography, and color palette of this image. Keep the description extremely concise (under 40 words). Focus on visual keywords."},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{encoded_string}"}
            ]
        )
        
        response = self.llm.invoke([message])
        return response.content.strip()