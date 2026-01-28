import os
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

class AIProcessor:
    def __init__(self):
        # We use Gemini 1.5 Flash - it's fast and supports Vision + Text
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def shortlist_news(self, news_list):
        """Uses AI to pick the most professional/viral story."""
        titles = "\n".join([f"- {n['title']}" for n in news_list])
        
        prompt = f"""
        Below is a list of AI news headlines from the last 24 hours.
        Pick the SINGLE MOST impactful story for a professional LinkedIn audience.
        Focus on: Innovation, Business Impact, or Future of Work.
        
        Headlines:
        {titles}
        
        Return ONLY the title of the chosen story.
        """
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def extract_style_from_image(self, image_path):
        """Vision: Analyzes a reference image to extract a prompt style."""
        img = Image.open(image_path)
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": "Describe the artistic style, lighting, and composition of this image. Provide a detailed prompt fragment that can be used to generate a new image in this exact style. Do not describe the subject, only the aesthetic."},
                {"type": "image_url", "image_url": image_path} # LangChain handles the conversion
            ]
        )
        
        response = self.llm.invoke([message])
        return response.content.strip()

# Testing logic
if __name__ == "__main__":
    # Mock data for testing
    sample_news = [{"title": "OpenAI releases Sora for everyone"}, {"title": "New causal inference study"}]
    proc = AIProcessor()
    print("Selected News:", proc.shortlist_news(sample_news))