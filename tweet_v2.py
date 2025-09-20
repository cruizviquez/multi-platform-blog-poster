import tweepy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create v2 client with Bearer Token
client = tweepy.Client(
    bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
)

# Send tweet using v2
try:
    response = client.create_tweet(text="Hello from my automated blog poster! 🚀")
    print(f"✅ Tweet posted successfully!")
    print(f"Tweet ID: {response.data['id']}")
except Exception as e:
    print(f"❌ Error: {e}")