# social_poster.py
import tweepy
from datetime import datetime
import json
from config import Config  # Add this import

class SocialMediaPoster:
    def __init__(self):
        self.platforms = {}
        self._setup_platforms()
    
    def _setup_platforms(self):
        # Setup Twitter/X with v2 API
        try:
            # Create v2 client (recommended for free tier)
            self.platforms['twitter'] = tweepy.Client(
                bearer_token=Config.TWITTER_BEARER_TOKEN,
                consumer_key=Config.TWITTER_API_KEY,
                consumer_secret=Config.TWITTER_API_SECRET,
                access_token=Config.TWITTER_ACCESS_TOKEN,
                access_token_secret=Config.TWITTER_ACCESS_SECRET
            )
            print("✓ Twitter connected (v2 API)")
            
            # Keep v1.1 API for features not in v2 (optional)
            auth = tweepy.OAuthHandler(
                Config.TWITTER_API_KEY, 
                Config.TWITTER_API_SECRET
            )
            auth.set_access_token(
                Config.TWITTER_ACCESS_TOKEN, 
                Config.TWITTER_ACCESS_SECRET
            )
            self.platforms['twitter_v1'] = tweepy.API(auth)
            
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
        # if 'linkedin' in self.platforms:
        #     results['linkedin'] = self.post_to_linkedin(post)
        
        return results
    
    def get_recent_tweets(self, count=5):
        """Get recent tweets (example of using the API)"""
        try:
            # Get authenticated user's ID
            me = self.platforms['twitter'].get_me()
            user_id = me.data.id
            
            # Get recent tweets
            tweets = self.platforms['twitter'].get_users_tweets(
                id=user_id, 
                max_results=count
            )
            
            return {'success': True, 'tweets': tweets.data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_tweet(self, tweet_id):
        """Delete a tweet by ID"""
        try:
            self.platforms['twitter'].delete_tweet(id=tweet_id)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}