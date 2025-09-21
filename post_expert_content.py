import json
from datetime import datetime
from social_poster import SocialMediaPoster

def post_expert_content():
    """Post expert content to Twitter and LinkedIn"""
    try:
        with open('expert_queue.json', 'r') as f:
            queue = json.load(f)
    except:
        print("❌ No expert content in queue")
        return
    
    if not queue:
        print("📭 Expert queue is empty")
        return
    
    # Get current time
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    # Find posts scheduled for this time (with 5-minute window)
    posts_to_send = []
    remaining = []
    
    for post in queue:
        if 'time_slot' in post:
            # Check if it's time to post (within 5 minutes)
            post_time = post['time_slot']
            if abs(int(post_time.split(':')[0]) - now.hour) == 0:
                if abs(int(post_time.split(':')[1]) - now.minute) <= 5:
                    posts_to_send.append(post)
                else:
                    remaining.append(post)
            else:
                remaining.append(post)
        else:
            # No time slot, post it now
            posts_to_send.append(post)
    
    if not posts_to_send:
        print(f"⏰ No posts scheduled for {current_time}")
        return
    
    # Initialize poster
    poster = SocialMediaPoster()
    
    # Post each
    for post in posts_to_send:
        print(f"\n📤 Posting: {post['content'][:60]}...")
        
                # Short posts work well as both tweet and LinkedIn post
        results = poster.post_to_all(
            title="",  # No title for short posts
            content=post['content'],
            url=""  # No URL for these expert posts
        )
        
        # Show results
        for platform, result in results.items():
            if result['success']:
                print(f"✅ {platform}: Posted successfully")
            else:
                print(f"❌ {platform}: {result['error']}")
    
    # Save remaining posts back to queue
    with open('expert_queue.json', 'w') as f:
        json.dump(remaining, f, indent=2)
    
    print(f"\n📋 {len(remaining)} posts remaining in queue")

if __name__ == "__main__":
    post_expert_content()