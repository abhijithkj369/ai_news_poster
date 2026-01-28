import os
from dotenv import load_dotenv

# Load env variables once here, so other files don't have to
load_dotenv()

# --- API KEYS ---
# We use .get() to avoid crashing if a key is missing during imports
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

# --- AI CONFIGURATION ---
# If Google changes the model name next year, you only edit this ONE line.
AI_MODEL_NAME = "gemini-2.5-flash" 
# AI_MODEL_NAME = "gemini-2.0-flash-lite-001" # Easy to swap!

# --- SCRAPER CONFIGURATION ---
# Centralize your target URLs. If Medium changes their URL, update it here.
URL_HACKER_NEWS = "https://news.ycombinator.com/list"
URL_MEDIUM_TAG = "https://medium.com/tag/artificial-intelligence/latest"
SEARCH_KEYWORDS = ['ai', 'gpt', 'llm', 'ml', 'nvidia', 'deepmind']

# --- GENERATOR CONFIGURATION ---
IMAGE_MODEL = "flux" # 'flux' or 'turbo'
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720