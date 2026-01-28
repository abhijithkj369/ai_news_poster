import os
import praw
from dotenv import load_dotenv

load_dotenv()

class RedditScraper:
    def __init__(self):
        # Initialize connection to Reddit using credentials from .env
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent="AI-News-Bot-v1.0 by /u/YourUsername"
        )

    def fetch_ai_trends(self, subreddit_name="ArtificialInteligence", limit=10):
        """Fetches top posts from the last 24 hours."""
        print(f"🔍 Searching r/{subreddit_name} for trends...")
        
        trending_posts = []
        subreddit = self.reddit.subreddit(subreddit_name)
        
        # We fetch 'hot' posts to see what people are talking about right now
        for post in subreddit.hot(limit=limit):
            # We skip 'Stickied' posts (usually rules/ads)
            if not post.stickied:
                trending_posts.append({
                    "title": post.title,
                    "score": post.score,
                    "url": post.url,
                    "text": post.selftext[:500] # Get first 500 chars of the body
                })
        
        return trending_posts

# This allows you to test the scraper individually without running the whole project
if __name__ == "__main__":
    scraper = RedditScraper()
    data = scraper.fetch_ai_trends()
    for i, post in enumerate(data, 1):
        print(f"{i}. {post['title']} (Score: {post['score']})")