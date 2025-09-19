# social_poster.py
import tweepy
from datetime import datetime
import json

class SocialMediaPoster:
    def __init__(self):
        self.platforms = {}
        self._setup_platforms()
    
    def _setup_platforms(self):
        # Setup Twitter/X
        try:
            auth = tweepy.OAuthHandler(
                Config.TWITTER_API_KEY, 
                Config.TWITTER_API_SECRET
            )
            auth.set_access_token(
                Config.TWITTER_ACCESS_TOKEN, 
                Config.TWITTER_ACCESS_SECRET
            )
            self.platforms['twitter'] = tweepy.API(auth)
            print("✓ Twitter connected")
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
        """Post to Twitter/X with 280 character limit"""
        try:
            # Format for Twitter
            tweet = f"{post['title']}\n\n{post['content'][:200]}...\n\n{post['url']}"
            
            # Ensure under 280 characters
            if len(tweet) > 280:
                tweet = f"{post['title'][:100]}...\n\n{post['url']}"
            
            # Post tweet
            response = self.platforms['twitter'].update_status(tweet)
            return {'success': True, 'id': response.id}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def post_to_all(self, title, content, url):
        """Post to all configured platforms"""
        post = self.create_post(title, content, url)
        results = {}
        
        if 'twitter' in self.platforms:
            results['twitter'] = self.post_to_twitter(post)
        
        # Add more platforms here
        
        return results
