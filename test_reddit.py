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
    
    # Test posting capability
    # Find a test subreddit
    test_sub = reddit.subreddit('test')
    print(f"✅ Can access r/{test_sub.display_name}")
    
except Exception as e:
    print(f"❌ Error: {e}")