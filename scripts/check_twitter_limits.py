# check_twitter_limits.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tweepy
from config import Config  # lowercase 'config'
from datetime import datetime

client = tweepy.Client(
    consumer_key=Config.TWITTER_API_KEY,
    consumer_secret=Config.TWITTER_API_SECRET,
    access_token=Config.TWITTER_ACCESS_TOKEN,
    access_token_secret=Config.TWITTER_ACCESS_SECRET
)

# Get rate limit status
try:
    me = client.get_me()
    print(f"✅ Connected as: @{me.data.username}")
    
    # Try to get tweets to see rate limit in headers
    tweets = client.get_users_tweets(me.data.id, max_results=5)
    print(f"📊 Recent tweets retrieved: {len(tweets.data) if tweets.data else 0}")
    
except tweepy.errors.TooManyRequests as e:
    # Get reset time from headers
    reset_timestamp = e.response.headers.get('x-rate-limit-reset')
    if reset_timestamp:
        reset_time = datetime.fromtimestamp(int(reset_timestamp))
        time_until_reset = reset_time - datetime.now()
        hours, remainder = divmod(time_until_reset.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        print(f"❌ Rate limited!")
        print(f"⏰ Resets at: {reset_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏳ Time until reset: {hours} hours, {minutes} minutes")
    else:
        print("❌ Rate limited (reset time unknown)")
except Exception as e:
    print(f"❌ Error: {e}")