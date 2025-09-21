# config.py
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