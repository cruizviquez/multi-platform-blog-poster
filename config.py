
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Twitter/X API credentials
    TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')
    TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN')
    
    # LinkedIn API credentials
    LINKEDIN_ACCESS_TOKEN = os.environ.get('LINKEDIN_ACCESS_TOKEN')
    LINKEDIN_USER_ID = os.environ.get('LINKEDIN_USER_ID')
    
    # Facebook API credentials
    FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID')
    FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
    
    # Groq AI
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    
    # SEO Platforms (optional)
    DEVTO_API_KEY = os.environ.get('DEVTO_API_KEY')
    MEDIUM_ACCESS_TOKEN = os.environ.get('MEDIUM_ACCESS_TOKEN')
    MEDIUM_USER_ID = os.environ.get('MEDIUM_USER_ID')
    
    # Dev.to
    DEVTO_API_KEY = os.environ.get('DEVTO_API_KEY')
    
    # Medium
    MEDIUM_ACCESS_TOKEN = os.environ.get('MEDIUM_ACCESS_TOKEN')
    MEDIUM_USER_ID = os.environ.get('MEDIUM_USER_ID')
    
    # Reddit
    REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')
    REDDIT_USERNAME = os.environ.get('REDDIT_USERNAME')
    REDDIT_PASSWORD = os.environ.get('REDDIT_PASSWORD')
    REDDIT_USER_AGENT = os.environ.get('REDDIT_USER_AGENT', 'BlogPoster/1.0')
    
    # Quora (uses Selenium - more complex)
    QUORA_EMAIL = os.environ.get('QUORA_EMAIL')
    QUORA_PASSWORD = os.environ.get('QUORA_PASSWORD')

    # Mastodon
    MASTODON_ACCESS_TOKEN = os.environ.get('MASTODON_ACCESS_TOKEN')
    MASTODON_INSTANCE_URL = os.environ.get('MASTODON_INSTANCE_URL', 'https://mastodon.social')