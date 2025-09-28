# test_reddit_simple.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import praw
from config import Config

reddit = praw.Reddit(
    client_id=Config.REDDIT_CLIENT_ID,
    client_secret=Config.REDDIT_CLIENT_SECRET,
    username=Config.REDDIT_USERNAME,
    password=Config.REDDIT_PASSWORD,
    user_agent=Config.REDDIT_USER_AGENT
)

# Test posting to known safe subreddits
safe_subs = ['test', 'bottesting', 'testingground4bots']

for sub_name in safe_subs:
    try:
        sub = reddit.subreddit(sub_name)
        print(f"\n✅ r/{sub_name} exists")
        
        # Try simple post
        submission = sub.submit(
            title="Test: Automated posting check",
            selftext="This is a test post from my blog automation tool. It will be deleted."
        )
        print(f"✅ Successfully posted: {submission.url}")
        
        # Delete immediately
        submission.delete()
        print("🗑️ Test post deleted")
        
        # This sub works!
        print(f"✅ r/{sub_name} WORKS for posting!\n")
        break
        
    except Exception as e:
        print(f"❌ r/{sub_name}: {e}")