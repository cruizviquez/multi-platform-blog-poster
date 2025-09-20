# social_poster.py
import tweepy
from datetime import datetime
import json
from config import Config

class SocialMediaPoster:
    def __init__(self):
        self.platforms = {}
        self._setup_platforms()
    
    def _setup_platforms(self):
        # Setup Twitter/X with v2 API
        try:
            # Only use v2 client
            self.platforms['twitter'] = tweepy.Client(
                consumer_key=Config.TWITTER_API_KEY,
                consumer_secret=Config.TWITTER_API_SECRET,
                access_token=Config.TWITTER_ACCESS_TOKEN,
                access_token_secret=Config.TWITTER_ACCESS_SECRET
            )
            print("✓ Twitter connected (v2 API)")
        except Exception as e:
            print(f"✗ Twitter connection failed: {e}")
    
    def create_post(self, title, content, url):
        """Create a post object with platform-specific formatting"""
        return {
            'title': title,
            'content': content,
            'url': url,
            'timestamp': datetime.now().isoformat()
        }
    
    def post_to_twitter(self, post):
        """Post to Twitter/X with 280 character limit using v2 API"""
        try:
            # Format for Twitter
            tweet = f"{post['title']}\n\n{post['content'][:200]}...\n\n{post['url']}"
            
            # Ensure under 280 characters
            if len(tweet) > 280:
                tweet = f"{post['title'][:100]}...\n\n{post['url']}"
            
            # Post tweet using v2 API
            response = self.platforms['twitter'].create_tweet(text=tweet)
            
            # Extract tweet ID from response
            tweet_id = response.data['id'] if response.data else None
            
            return {'success': True, 'id': tweet_id, 'text': tweet}
        
        except tweepy.TweepyException as e:
            return {'success': False, 'error': str(e)}
        except Exception as e:
            return {'success': False, 'error': f"Unexpected error: {str(e)}"}
    
    def post_to_all(self, title, content, url):
        """Post to all configured platforms"""
        post = self.create_post(title, content, url)
        results = {}
        
        if 'twitter' in self.platforms:
            results['twitter'] = self.post_to_twitter(post)
        
        # Add more platforms here
        
        return results