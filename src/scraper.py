import requests
from bs4 import BeautifulSoup
import time

class NewsScraper:
    def __init__(self):
        # We use a browser-like User-Agent to avoid being blocked
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }

    def fetch_hacker_news_ai(self, limit=5):
        """Scrapes Hacker News for AI-related stories."""
        url = "https://news.ycombinator.com/list"
        print(f"🕵️‍♂️ Scraping Hacker News...")
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = []
            items = soup.find_all('tr', class_='athing', limit=30) 
            for item in items:
                title_line = item.find('span', class_='titleline')
                if title_line:
                    title = title_line.text
                    link = title_line.find('a')['href']
                    if any(word in title.lower() for word in ['ai', 'gpt', 'llm', 'ml']):
                        articles.append({"title": title, "url": link, "source": "Hacker News"})
                if len(articles) >= limit: break
            return articles
        except Exception as e:
            print(f"⚠️ HN Error: {e}")
            return []

    def fetch_medium_ai(self, limit=5):
        """Scrapes Medium's 'Artificial Intelligence' tag page."""
        # Using the 'latest' feed for the most recent trends
        url = "https://medium.com/tag/artificial-intelligence/latest"
        print(f"🕵️‍♂️ Scraping Medium AI Trends...")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = []
            
            # Medium logic: Look for article tags or h2 headers which usually contain titles
            # Note: Medium changes classes often, so we target the 'article' tag directly
            posts = soup.find_all('article', limit=15)
            
            for post in posts:
                # Find the title (usually in an h2)
                title_tag = post.find('h2')
                # Find the link (the first <a> that contains the title or is near it)
                link_tag = post.find('a', href=True)
                
                if title_tag and link_tag:
                    title = title_tag.get_text().strip()
                    # Ensure the link is a full URL
                    link = link_tag['href']
                    if link.startswith('/'):
                        link = f"https://medium.com{link}"
                    
                    articles.append({
                        "title": title,
                        "url": link,
                        "source": "Medium"
                    })
                
                if len(articles) >= limit:
                    break
            return articles
        except Exception as e:
            print(f"⚠️ Medium Error: {e}")
            return []

# --- TESTING BLOCK ---
if __name__ == "__main__":
    scraper = NewsScraper()
    
    # Test Hacker News
    hn_results = scraper.fetch_hacker_news_ai(limit=3)
    print(f"\n✅ Found {len(hn_results)} stories on Hacker News")
    
    # Test Medium
    medium_results = scraper.fetch_medium_ai(limit=3)
    print(f"✅ Found {len(medium_results)} stories on Medium")
    
    # Combine and display
    all_news = hn_results + medium_results
    print("\n--- LATEST AI TRENDS REPORT ---")
    for i, news in enumerate(all_news, 1):
        print(f"{i}. [{news['source']}] {news['title']}")
        print(f"   URL: {news['url']}\n")