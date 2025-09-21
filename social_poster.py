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
        
        # Setup LinkedIn
        if hasattr(Config, 'LINKEDIN_ACCESS_TOKEN') and Config.LINKEDIN_ACCESS_TOKEN:
            self.platforms['linkedin'] = {
                'token': Config.LINKEDIN_ACCESS_TOKEN,
                'user_id': Config.LINKEDIN_USER_ID
            }
            print("✓ LinkedIn connected")
        else:
            print("ℹ️  LinkedIn not configured (no credentials)")
        
        # Setup Facebook
        if hasattr(Config, 'FACEBOOK_ACCESS_TOKEN') and Config.FACEBOOK_ACCESS_TOKEN:
            self.platforms['facebook'] = {
                'token': Config.FACEBOOK_ACCESS_TOKEN,
                'page_id': Config.FACEBOOK_PAGE_ID
            }
            print("✓ Facebook connected")
        else:
            print("ℹ️  Facebook not configured (no credentials)")
    
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
            if post['title'] and post['url']:
                tweet = f"{post['title']}\n\n{post['content'][:200]}...\n\n{post['url']}"
            elif post['content'] and post['url']:
                tweet = f"{post['content']}\n\n{post['url']}"
            else:
                tweet = post['content']  # For expert short posts
            
            # Ensure under 280 characters
            if len(tweet) > 280:
                if post['url']:
                    tweet = f"{post['title'][:100]}...\n\n{post['url']}"
                else:
                    tweet = tweet[:280]
            
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
            if post['title'] and post['url']:
                linkedin_text = f"{post['title']}\n\n{post['content']}\n\n{post['url']}"
            elif post['content']:
                linkedin_text = post['content']
            else:
                linkedin_text = post['title'] if post['title'] else ""
            
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
    
    def post_to_facebook(self, post):
        """Post to Facebook Page"""
        try:
            # Format content for Facebook
            if post['title'] and post['url']:
                message = f"{post['title']}\n\n{post['content']}\n\n{post['url']}"
            elif post['content']:
                message = post['content']
            else:
                message = post['title'] if post['title'] else ""
            
            # Facebook Graph API endpoint
            url = f"https://graph.facebook.com/v18.0/{self.platforms['facebook']['page_id']}/feed"
            
            params = {
                'message': message,
                'access_token': self.platforms['facebook']['token']
            }
            
            # If there's a URL, add it as a link
            if post.get('url'):
                params['link'] = post['url']
            
            response = requests.post(url, data=params)
            
            if response.status_code == 200:
                result = response.json()
                return {'success': True, 'id': result.get('id')}
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
        
        if 'facebook' in self.platforms:
            results['facebook'] = self.post_to_facebook(post)
        
        return results
    
    def get_enabled_platforms(self):
        """Return list of enabled platforms"""
        return list(self.platforms.keys())
    
    def post_short_content(self, content, platforms=None):
        """Post short-form content to specific platforms or all"""
        if platforms is None:
            platforms = self.get_enabled_platforms()
        
        post = self.create_post("", content, "")
        results = {}
        
        if 'twitter' in platforms and 'twitter' in self.platforms:
            results['twitter'] = self.post_to_twitter(post)
        
        if 'linkedin' in platforms and 'linkedin' in self.platforms:
            results['linkedin'] = self.post_to_linkedin(post)
        
        if 'facebook' in platforms and 'facebook' in self.platforms:
            results['facebook'] = self.post_to_facebook(post)
        
        return results