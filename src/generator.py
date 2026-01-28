import requests
import time
import os

class ImageGenerator:
    def __init__(self):
        # We use a reliable, free inference API for the FLUX model
        self.base_url = "https://image.pollinations.ai/prompt"

    def generate_image(self, news_title, style_prompt):
        """
        Combines the News Title + Style Prompt to generate an image.
        Returns the filename of the saved image.
        """
        print("🎨 Constructing image prompt...")
        
        # 1. Create a "Prompt Engineering" structure
        # We keep the news subject central, but wrap it in the extracted style
        final_prompt = f"Editorial illustration for news about: {news_title}. {style_prompt}. High quality, trending on artstation, 8k resolution, cinematic lighting."
        
        # URL encode the prompt so it travels safely over the internet
        encoded_prompt = requests.utils.quote(final_prompt)
        
        # 2. Build the request URL (using FLUX model for realism)
        # Random seed ensures we get a new image every time
        seed = int(time.time())
        image_url = f"{self.base_url}/{encoded_prompt}?width=1280&height=720&model=flux&seed={seed}&nologo=true"
        
        print(f"🖌️  Requesting Image Generation (Model: FLUX)...")
        
        try:
            # 3. Fetch the image bytes
            response = requests.get(image_url, timeout=30)
            
            if response.status_code == 200:
                # 4. Save to disk
                filename = f"post_image_{seed}.jpg"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Image saved successfully: {filename}")
                return filename
            else:
                print(f"❌ API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return None

# Testing logic
if __name__ == "__main__":
    gen = ImageGenerator()
    gen.generate_image("Artificial General Intelligence is here", "Cyberpunk neon style, dark background, glowing blue circuits")