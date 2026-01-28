import os
from dotenv import load_dotenv
from src.scraper import NewsScraper
from src.processor import AIProcessor
from src.generator import ImageGenerator  # <--- NEW IMPORT

def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found!")
        return

    print("🚀 Initializing AI News Pipeline...")
    
    scraper = NewsScraper()
    processor = AIProcessor(api_key=api_key)
    generator = ImageGenerator() # <--- NEW INITIALIZATION

    try:
        # 1. Scraping
        print("📥 Fetching latest AI trends...")
        hn_news = scraper.fetch_hacker_news_ai(limit=3)
        medium_news = scraper.fetch_medium_ai(limit=3)
        all_news = hn_news + medium_news
        
        if not all_news:
            print("⚠️ No news found.")
            return

        # 2. Shortlisting
        print(f"🧠 Analyzing {len(all_news)} stories...")
        selected_story = processor.shortlist_news(all_news)
        print(f"\n🏆 TOPIC: {selected_story}\n")

        # 3. Vision (Style Extraction)
        style_prompt = "Futuristic, high-tech, minimal, 3d render, isometric" # Default fallback
        
        if os.path.exists("reference.png"):
            print("👁️  analyzing reference image for style...")
            try:
                # Note: If gemini-2.0-flash-lite fails on images, we might need gemini-2.5-flash
                style_prompt = processor.extract_style_from_image("reference.png")
                print(f"✨ Style Extracted: {style_prompt[:80]}...")
            except Exception as e:
                print(f"⚠️ Vision Error (Using default style): {e}")
        else:
            print("💡 No 'reference.png' found. Using default 'Futuristic' style.")

        # 4. Generation
        print("🎨 Generating final LinkedIn Post Image...")
        final_image = generator.generate_image(selected_story, style_prompt)
        
        if final_image:
            print("\n" + "="*40)
            print(f"✅ PROJECT SUCCESS! Image ready: {final_image}")
            print(f"📝 Post Title: {selected_story}")
            print("="*40 + "\n")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()