import os
from dotenv import load_dotenv
from src.scraper import NewsScraper
from src.processor import AIProcessor

def main():
    # 1. Load configuration and keys
    load_dotenv()
    print("🚀 Initializing AI News Pipeline...")
    
    # Initialize our modules
    scraper = NewsScraper()
    processor = AIProcessor()

    try:
        # 2. Extraction Phase (Scraping)
        print("📥 Fetching latest AI trends from Medium and Hacker News...")
        hn_news = scraper.fetch_hacker_news_ai(limit=3)
        medium_news = scraper.fetch_medium_ai(limit=3)
        
        all_news = hn_news + medium_news
        
        if not all_news:
            print("⚠️ No news found. Check your internet or selectors.")
            return

        # 3. Processing Phase (Shortlisting)
        print(f"🧠 Analyzing {len(all_news)} stories to find the best one...")
        selected_story = processor.shortlist_news(all_news)
        
        print("\n" + "="*30)
        print(f"🏆 WINNING STORY: {selected_story}")
        print("="*30 + "\n")

        # 4. Style Extraction (Vision) - We'll assume you have a 'ref.jpg'
        # To test this, place any image in your root folder named 'reference.jpg'
        if os.path.exists("reference.jpg"):
            print("🎨 Extracting style from reference image...")
            style_prompt = processor.extract_style_from_image("reference.jpg")
            print(f"✨ Extracted Style: {style_prompt[:100]}...")
        else:
            print("💡 No 'reference.jpg' found. Skipping vision step for now.")

    except Exception as e:
        print(f"❌ An error occurred in the pipeline: {e}")

if __name__ == "__main__":
    main()