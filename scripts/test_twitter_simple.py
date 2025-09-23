# test_twitter_simple.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tweepy
from config import Config

print("Testing Twitter connection...")

client = tweepy.Client(
    consumer_key=Config.TWITTER_API_KEY,
    consumer_secret=Config.TWITTER_API_SECRET,
    access_token=Config.TWITTER_ACCESS_TOKEN,
    access_token_secret=Config.TWITTER_ACCESS_SECRET
)

try:
    # Test 1: Get user info (this worked)
    me = client.get_me()
    print(f"✅ Step 1 - Connected as: @{me.data.username}")
    
    # Test 2: Try to post
    response = client.create_tweet(text="Test from my automation tool - checking permissions")
    print(f"✅ Step 2 - Tweet posted! ID: {response.data['id']}")
    
except tweepy.errors.Forbidden as e:
    print(f"❌ Forbidden: {e}")
    print("Your app doesn't have tweet posting permissions")
    
except tweepy.errors.TooManyRequests as e:
    print(f"❌ Rate limited: {e}")
    
except tweepy.errors.Unauthorized as e:
    print(f"❌ Unauthorized: {e}")
    print("Token might be expired or invalid")
    
except Exception as e:
    print(f"❌ Other error: {type(e).__name__}: {e}")