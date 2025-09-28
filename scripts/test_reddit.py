# test_reddit.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import praw
from config import Config

print("Testing Reddit connection...")

try:
    reddit = praw.Reddit(
        client_id=Config.REDDIT_CLIENT_ID,
        client_secret=Config.REDDIT_CLIENT_SECRET,
        username=Config.REDDIT_USERNAME,
        password=Config.REDDIT_PASSWORD,
        user_agent=Config.REDDIT_USER_AGENT
    )
    
    # Test authentication
    user = reddit.user.me()
    print(f"✅ Connected as: /u/{user.name}")
    print(f"Karma: {user.link_karma} link | {user.comment_karma} comment")
    
    # Test access to configured subreddits
    print("\n📋 Checking configured subreddits:")
    for content_type, sub_name in Config.REDDIT_SUBREDDITS.items():
        try:
            sub = reddit.subreddit(sub_name)
            print(f"✅ r/{sub_name}: {sub.subscribers:,} subscribers")
        except Exception as e:
            print(f"❌ r/{sub_name}: Cannot access")
    
except Exception as e:
    print(f"❌ Error: {e}")