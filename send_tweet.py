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

# Send tweet
try:
    tweet = api.update_status("Hello from my automated blog poster! 🚀")
    print(f"✅ Tweet posted successfully!")
    print(f"View at: https://twitter.com/user/status/{tweet.id}")
except Exception as e:
    print(f"❌ Error posting tweet: {e}")