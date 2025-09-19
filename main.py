# main.py
from social_poster import SocialMediaPoster
import schedule
import time

def main():
    poster = SocialMediaPoster()
    
    # Example: Post a blog article
    results = poster.post_to_all(
        title="My Latest Blog Post: Python Tips",
        content="Here are 5 Python tips that will save you hours of coding time...",
        url="https://yourblog.com/python-tips"
    )
    
    print("Posting results:", results)

def scheduled_post():
    """Example of scheduled posting"""
    poster = SocialMediaPoster()
    
    # Read from a content queue file
    with open('content_queue.json', 'r') as f:
        posts = json.load(f)
    
    if posts:
        next_post = posts.pop(0)
        results = poster.post_to_all(**next_post)
        print(f"Posted: {next_post['title']}")
        
        # Save remaining posts
        with open('content_queue.json', 'w') as f:
            json.dump(posts, f)

if __name__ == "__main__":
    # Run once
    main()
    
    # Or schedule posts
    # schedule.every().day.at("09:00").do(scheduled_post)
    # schedule.every().day.at("15:00").do(scheduled_post)
    # 
    # while True:
    #     schedule.run_pending()

  
  
  #     time.sleep(60)
