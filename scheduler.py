# scheduler.py
import schedule
import time
import json
from datetime import datetime
from social_poster import SocialMediaPoster

class ContentScheduler:
    def __init__(self, queue_file='content_queue.json'):
        self.queue_file = queue_file
        self.poster = SocialMediaPoster()
        
    def load_queue(self):
        """Load posts from queue file"""
        try:
            with open(self.queue_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_queue(self, posts):
        """Save remaining posts"""
        with open(self.queue_file, 'w') as f:
            json.dump(posts, f, indent=2)
    
    def post_next(self):
        """Post the next item in queue"""
        posts = self.load_queue()
        
        if not posts:
            print("📭 No posts in queue")
            return
        
        # Get next post
        next_post = posts.pop(0)
        print(f"\n📤 Posting: {next_post['title']}")
        
        # Post to all platforms
        results = self.poster.post_to_all(
            title=next_post['title'],
            content=next_post['content'],
            url=next_post['url']
        )
        
        # Log results
        for platform, result in results.items():
            if result['success']:
                print(f"✅ {platform}: Posted successfully")
            else:
                print(f"❌ {platform}: {result['error']}")
        
        # Save remaining posts
        self.save_queue(posts)
        
        # Log to history
        self.log_post(next_post, results)
    
    def log_post(self, post, results):
        """Keep history of posted content"""
        history = {
            'timestamp': datetime.now().isoformat(),
            'post': post,
            'results': results
        }
        
        # Append to history file
        try:
            with open('post_history.json', 'r') as f:
                history_list = json.load(f)
        except:
            history_list = []
        
        history_list.append(history)
        
        with open('post_history.json', 'w') as f:
            json.dump(history_list, f, indent=2)

def run_scheduler():
    """Main scheduler function"""
    scheduler = ContentScheduler()
    
    # Schedule posts at specific times
    # Daily posts at 9 AM, 1 PM, and 6 PM
    schedule.every().day.at("09:00").do(scheduler.post_next)
    schedule.every().day.at("13:00").do(scheduler.post_next)
    schedule.every().day.at("18:00").do(scheduler.post_next)
    
    # Or post every X hours
    # schedule.every(4).hours.do(scheduler.post_next)
    
    print("📅 Scheduler started!")
    print("Posting times: 9:00 AM, 1:00 PM, 6:00 PM")
    print("Press Ctrl+C to stop\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    run_scheduler()