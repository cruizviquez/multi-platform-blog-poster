import tweepy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Setup authentication
auth = tweepy.OAuthHandler(
    os.getenv('TWITTER_API_KEY'),
    os.getenv('TWITTER_API_SECRET')
)
auth.set_access_token(
    os.getenv('TWITTER_ACCESS_TOKEN'),
    os.getenv('TWITTER_ACCESS_SECRET')
)

# Create API object
api = tweepy.API(auth)

# Test - Get your username
try:
    user = api.verify_credentials()
    print(f"✅ Connected as: @{user.screen_name}")
except Exception as e:
    print(f"❌ Error: {e}")
