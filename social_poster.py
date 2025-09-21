import tweepy
import requests
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
            self.platforms['twitter'] = tweepy.Client(
                consumer_key=Config.TWITTER_API_KEY,
                consumer_secret=Config.TWITTER_API_SECRET,
                access_token=Config.TWITTER_ACCESS_TOKEN,
                access_token_secret=Config.TWITTER_ACCESS_SECRET
            )
            print("✓ Twitter connected (v2 API)")
        except Exception as e:
            print(f"✗ Twitter connection failed: {e}")
        
        # Setup LinkedIn - only if credentials exist
        if hasattr(Config, 'LINKEDIN_ACCESS_TOKEN') and Config.LINKEDIN_ACCESS_TOKEN:
            self.platforms['linkedin'] = {
                'token': Config.LINKEDIN_ACCESS_TOKEN,
                'user_id': Config.LINKEDIN_USER_ID
            }
            print("✓ LinkedIn connected")
        else:
            print("ℹ️  LinkedIn not configured (no credentials)")
    
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
    
    def post_to_linkedin(self, post):
        """Post to LinkedIn"""
        try:
            headers = {
                'Authorization': f'Bearer {self.platforms["linkedin"]["token"]}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            
            # Format content for LinkedIn
            linkedin_text = f"{post['title']}\n\n{post['content']}\n\n{post['url']}"
            
            # LinkedIn API payload
            data = {
                "author": f"urn:li:person:{self.platforms['linkedin']['user_id']}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": linkedin_text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(
                'https://api.linkedin.com/v2/ugcPosts',
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                return {'success': True, 'id': response.headers.get('x-restli-id')}
            else:
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def post_to_all(self, title, content, url):
        """Post to all configured platforms"""
        post = self.create_post(title, content, url)
        results = {}
        
        if 'twitter' in self.platforms:
            results['twitter'] = self.post_to_twitter(post)
        
        if 'linkedin' in self.platforms:
            results['linkedin'] = self.post_to_linkedin(post)
        
        return results
    
    def post_short_content(self, content):
    """Post short-form content optimized for engagement"""
    results = {}
    
    # Twitter - posts as-is
    if 'twitter' in self.platforms:
        try:
            response = self.platforms['twitter'].create_tweet(text=content)
            tweet_id = response.data['id'] if response.data else None
            results['twitter'] = {'success': True, 'id': tweet_id}
        except Exception as e:
            results['twitter'] = {'success': False, 'error': str(e)}
    
    # LinkedIn - same content works
    if 'linkedin' in self.platforms:
        results['linkedin'] = self.post_to_linkedin({
            'title': '',
            'content': content,
            'url': ''
        })
    
    return results