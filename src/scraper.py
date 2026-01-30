import feedparser
import sys
import os

# Fix path so we can import config if running this file directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

class NewsScraper:
    def __init__(self):
        # We use RSS feeds which are much more stable than HTML scraping
        self.feeds = [
            "https://hnrss.org/newest?q=AI+OR+LLM+OR+GPT", # Hacker News AI Feed
            "https://www.theverge.com/rss/artificial-intelligence/index.xml", # The Verge AI
            "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml" # NYT Tech
        ]

    def fetch_hacker_news_ai(self, limit=5):
        """Fetches from RSS feeds instead of raw HTML scraping."""
        print(f"📡 Polling RSS Feeds for latest AI news...")
        articles = []
        
        for url in self.feeds:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]:
                    # Broad filter to capture more news
                    if any(x in entry.title.lower() for x in ['ai', 'gpt', 'llm', 'model', 'intelligence', 'nvidia', 'tech', 'data']):
                        articles.append({
                            "title": entry.title,
                            "url": entry.link,
                            "source": "RSS Feed"
                        })
            except Exception as e:
                print(f"⚠️ RSS Error for {url}: {e}")
                
            if len(articles) >= limit: 
                break
                
        return articles

    def fetch_medium_ai(self, limit=5):
        return [] # We rely on the RSS feeds above

# Debug block
if __name__ == "__main__":
    scraper = NewsScraper()
    news = scraper.fetch_hacker_news_ai()
    print(f"\n✅ Found {len(news)} stories:")
    for n in news:
        print(f"- {n['title']}")