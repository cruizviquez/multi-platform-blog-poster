import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tweepy
import requests
from datetime import datetime
import json
from config import Config  # Now it can find config.py in root
import time


from core.social_poster import SocialMediaPoster
def load_expert_queue():
    """Load posts from expert queue"""
    import os
    
    # Try multiple locations
    possible_paths = [
        'expert_queue.json',
        'core/expert_queue.json',
        os.path.join(os.path.dirname(__file__), '..', 'core', 'expert_queue.json')
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    queue = json.load(f)
                    print(f"✅ Loaded {len(queue)} posts from {path}")
                    return queue
            except Exception as e:
                print(f"❌ Error reading {path}: {e}")
    
    print("❌ No expert_queue.json found in any expected location")
    return []

def save_expert_queue(queue):
    """Save updated queue"""
    with open('expert_queue.json', 'w') as f:
        json.dump(queue, f, indent=2)

def post_next_expert_content():
    """Post the next item from expert queue"""
    queue = load_expert_queue()
    
    if not queue:
        print(f"📭 {datetime.now().strftime('%H:%M')} - No posts in expert queue")
        return False
    
    # Get next post (ignore scheduled times)
    next_post = queue.pop(0)
    
    print(f"\n📤 {datetime.now().strftime('%H:%M')} - Posting: {next_post['content'][:60]}...")
    
    # Post it
    poster = SocialMediaPoster()
    
    # For short posts, use simplified posting
    results = poster.post_to_all(
        title="",
        content=next_post['content'],
        url=""
    )
    
    # Show results
    success = False
    for platform, result in results.items():
        if result['success']:
            print(f"✅ {platform}: Posted")
            success = True
        else:
            print(f"❌ {platform}: {result['error']}")
    
    if success:
        # Save updated queue
        save_expert_queue(queue)
        print(f"📋 {len(queue)} posts remaining")
    else:
        # Put post back if failed
        queue.insert(0, next_post)
        save_expert_queue(queue)
        print("⚠️ Post returned to queue due to errors")
    
    return success

def run_interval_poster(interval_minutes=30):
    """Post every X minutes"""
    print(f"🤖 Interval Poster Started")
    print(f"⏰ Will post every {interval_minutes} minutes")
    print(f"📅 Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("Press Ctrl+C to stop\n")
    
    while True:
        try:
            # Post content
            post_next_expert_content()
            
            # Wait for next interval
            print(f"\n💤 Sleeping {interval_minutes} minutes until next post...")
            time.sleep(interval_minutes * 60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interval poster stopped by user")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print(f"⏳ Waiting {interval_minutes} minutes before retry...")
            time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    import sys
    
    # Check if custom interval provided
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except:
            interval = 30
    else:
        interval = 30
    
    run_interval_poster(interval_minutes=interval)