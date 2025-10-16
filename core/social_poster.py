# social_poster.py
import tweepy
import requests
import praw
from datetime import datetime
import json
from config import Config
import os
from mastodon import Mastodon


class SocialMediaPoster:
    def __init__(self):
        self.platforms = {}
        self._setup_platforms()

    def _setup_platforms(self):
        # Setup Mastodon
        if hasattr(
            Config, 'MASTODON_ACCESS_TOKEN') and Config.MASTODON_ACCESS_TOKEN:
            try:
                self.platforms['mastodon'] = Mastodon(
                access_token=Config.MASTODON_ACCESS_TOKEN,
                api_base_url=Config.MASTODON_INSTANCE_URL
            )
                print("✓ Mastodon connected")
            except Exception as e:
                print(f"✗ Mastodon connection failed: {e}")

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
        if hasattr(
            Config, 'LINKEDIN_ACCESS_TOKEN') and Config.LINKEDIN_ACCESS_TOKEN:
            self.platforms['linkedin'] = {
                'token': Config.LINKEDIN_ACCESS_TOKEN,
                'user_id': Config.LINKEDIN_USER_ID
            }
            print("✓ LinkedIn connected")
        else:
            print("ℹ️  LinkedIn not configured (no credentials)")

        # Setup Facebook
        if hasattr(
            Config, 'FACEBOOK_ACCESS_TOKEN') and Config.FACEBOOK_ACCESS_TOKEN:
            self.platforms['facebook'] = {
                'token': Config.FACEBOOK_ACCESS_TOKEN,
                'page_id': Config.FACEBOOK_PAGE_ID
            }
            print("✓ Facebook connected")
        else:
            print("ℹ️  Facebook not configured (no credentials)")

        # Setup Dev.to
        if hasattr(Config, 'DEVTO_API_KEY') and Config.DEVTO_API_KEY:
            self.platforms['devto'] = {
                'api_key': Config.DEVTO_API_KEY
            }
            print("✓ Dev.to connected")
        else:
            print("ℹ️  Dev.to not configured")

        # Setup Medium
        if hasattr(Config, 'MEDIUM_ACCESS_TOKEN') and Config.MEDIUM_ACCESS_TOKEN:
            self.platforms['medium'] = {
                'token': Config.MEDIUM_ACCESS_TOKEN,
                'user_id': Config.MEDIUM_USER_ID
            }
            print("✓ Medium connected")
        else:
            print("ℹ️  Medium not configured")

        # Setup Reddit
        if hasattr(Config, 'REDDIT_CLIENT_ID') and Config.REDDIT_CLIENT_ID:
            try:
                self.platforms['reddit'] = praw.Reddit(
                    client_id=Config.REDDIT_CLIENT_ID,
                    client_secret=Config.REDDIT_CLIENT_SECRET,
                    username=Config.REDDIT_USERNAME,
                    password=Config.REDDIT_PASSWORD,
                    user_agent=Config.REDDIT_USER_AGENT
                )
                print("✓ Reddit connected")
            except Exception as e:
                print(f"✗ Reddit connection failed: {e}")

    def create_post(self, title, content, url):
        """Create a post object with platform-specific formatting"""
        return {
            'title': title,
            'content': content,
            'url': url,
            'timestamp': datetime.now().isoformat()
        }

    def expand_content_for_platform(self, post, platform):
        """Expand short content to longer form for certain platforms"""
        if platform in ['twitter', 'facebook']:
            # Keep short for Twitter/Facebook
            return post['content']

        # For platforms that support longer content
        if not hasattr(self, 'groq_client'):
            # Initialize Groq for content expansion
            from groq import Groq
            # Remove proxy issues
            for proxy_var in ['http_proxy', 'https_proxy',
                'HTTP_PROXY', 'HTTPS_PROXY', 'proxies']:
                os.environ.pop(proxy_var, None)
            self.groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        try:
            # Expand content using AI
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI/ML expert. Expand the following short insight into a detailed, engaging post (800-1000 characters). Keep the same tone and add valuable details, examples, or explanations."
                    },
                    {
                        "role": "user",
                        "content": f"Expand this into 800-1000 characters:\n\n{post['content']}"
                    }
                ],
                temperature=0.7,
                max_tokens=300
            )

            expanded = response.choices[0].message.content.strip()

            # Ensure it's not too long
            if len(expanded) > 1000:
                expanded = expanded[:997] + "..."

            return expanded

        except Exception as e:
            print(f"⚠️  Expansion failed, using original: {e}")
            return post['content']

    def _truncate_logical(self, text, max_length):
        """Truncate text at last full sentence or word within max_length."""
        if len(text) <= max_length:
            return text
        truncated = text[:max_length]
        # Try to end at last period, exclamation, or question mark
        for end in ['.', '!', '?']:
            idx = truncated.rfind(end)
            if idx != -1 and idx > max_length // 2:
                return truncated[:idx+1]
        # Otherwise, end at last space
        idx = truncated.rfind(' ')
        if idx != -1 and idx > max_length // 2:
            return truncated[:idx] + '...'
        # Fallback: hard cut
        return truncated.rstrip() + '...'

    def post_to_mastodon(self, post):
        """Post to Mastodon"""
        try:
            # For Mastodon, we need to respect 500 char limit but make it complete
            if post['title'] and post['url']:
                url_len = len(post['url']) + 4
                title_len = len(post['title']) + 4
                available = 500 - url_len - title_len - 10
                content = self._truncate_logical(post['content'], available)
                mastodon_text = f"{post['title']}\n\n{content}\n\n{post['url']}"
            else:
                content = post['content'].strip('"\'')
                content = self._truncate_logical(content, 500)
                mastodon_text = content
            status = self.platforms['mastodon'].status_post(
                mastodon_text,
                visibility='public'
            )
            return {
                'success': True,
                'id': status['id'],
                'url': status['url']
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def post_to_twitter(self, post):
        """Post to Twitter/X with 280 character limit using v2 API"""
        try:
            # Format for Twitter
            if post['title'] and post['url']:
                base = f"{post['title']}\n\n{post['content']}\n\n{post['url']}"
            elif post['content'] and post['url']:
                base = f"{post['content']}\n\n{post['url']}"
            else:
                base = post['content'].strip('"\'')

            tweet = self._truncate_logical(base, 280)

            # Post tweet using v2 API
            response = self.platforms['twitter'].create_tweet(text=tweet)

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
            
            # LinkedIn allows long posts - use expanded content
            if post.get('content'):
                # For expert posts, expand them for LinkedIn
                expanded = self.expand_content_for_platform(post, 'linkedin')
                linkedin_text = self._truncate_logical(expanded, 1300)
            else:
                # For regular posts
                linkedin_text = f"{post['title']}\n\n{post['content']}\n\n{post['url']}"
            
            # Remove quotes
            linkedin_text = linkedin_text.strip('"\'')
            
            # LinkedIn API payload
            data = {
                "author": f"urn:li:person:{self.platforms['linkedin']['user_id']}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": linkedin_text  # No truncation needed for LinkedIn
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
                message = f"{
    post['title']}\n\n{
        post['content']}\n\n{
            post['url']}"
            elif post['content']:
                message = post['content'].strip('"\'')  # Remove quotes
            else:
                message = post['title'] if post['title'] else ""

            # Facebook Graph API endpoint
            url = f"https://graph.facebook.com/v18.0/{
    self.platforms['facebook']['page_id']}/feed"

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

    def post_to_devto(self, post):
        """Post to Dev.to as an article"""
        try:
            headers = {
                'api-key': self.platforms['devto']['api_key'],
                'Content-Type': 'application/json'
            }

            # Expand content for Dev.to
            expanded_content = self.expand_content_for_platform(post, 'devto')

            # Create a title from the first part of content
            title = post.get('title', '')
            if not title:
                # Generate title from content
                title = expanded_content[:60].strip()
                if '.' in title:
                    title = title.split('.')[0]
                title = title.strip('.,!?')

            # Format as article
            article_content = f"""
{expanded_content}

---

*This post was originally shared as an AI/ML insight. Follow me for more expert content on artificial intelligence and machine learning.*
"""

            article_data = {
                'article': {
                    'title': title,
                    'body_markdown': article_content,
                    'tags': ['ai', 'machinelearning', 'technology', 'programming'],
                    'published': True
                }
            }

            response = requests.post(
                'https://dev.to/api/articles',
                headers=headers,
                json=article_data
            )

            if response.status_code == 201:
                result = response.json()
                return {'success': True,
                    'id': result['id'], 'url': result['url']}
            else:
                return {'success': False, 'error': response.text}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def post_to_medium(self, post):
        """Post to Medium"""
        try:
            headers = {
                'Authorization': f'Bearer {self.platforms["medium"]["token"]}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            # Expand content for Medium
            expanded_content = self.expand_content_for_platform(post, 'medium')

            # Generate title
            title = post.get('title', expanded_content[:60] + '...')

            # Format for Medium
            content_html = f"""
<p>{expanded_content}</p>
<hr>
<p><em>Follow me for more AI/ML insights and tutorials.</em></p>
"""

            article_data = {
                'title': title,
                'contentFormat': 'html',
                'content': content_html,
                'tags': ['artificial-intelligence', 'machine-learning', 'technology'],
                'publishStatus': 'public'
            }

            response = requests.post(
                f'https://api.medium.com/v1/users/{
    self.platforms["medium"]["user_id"]}/posts',
                headers=headers,
                json=article_data
            )

            if response.status_code == 201:
                result = response.json()
                return {'success': True,
                    'id': result['data']['id'], 'url': result['data']['url']}
            else:
                return {'success': False, 'error': response.text}

        except Exception as e:
            return {'success': False, 'error': str(e)}
        
    def post_to_reddit(self, post, subreddit=None):
        """Post to Reddit"""
        try:
            reddit = self.platforms['reddit']
            
            # Subreddits that only allow links (no text posts)
            LINK_ONLY_SUBS = ['todayilearned', 'technology', 'science']
            
            # Subreddits that allow text posts
            TEXT_ALLOWED_SUBS = ['unpopularopinion', 'test', 'AskReddit', 
                                'testingground4bots', 'self', 'discussion']
            
            # Determine subreddit
            if not subreddit:
                content_type = post.get('type', 'default')
                # Use text-allowed subreddits for our posts
                if content_type in ['unpopularopinion', 'hot_take', 'prediction']:
                    subreddit = 'unpopularopinion'
                elif content_type in ['code_snippet', 'challenge']:
                    subreddit = 'test'  # dailyprogrammer might need specific format
                else:
                    subreddit = 'test'  # Safe default that allows text
            
            print(f"📮 Posting to r/{subreddit}")
            
            sub = reddit.subreddit(subreddit)
            
            # Expand content
            expanded_content = self.expand_content_for_platform(post, 'reddit')
            
            # Generate title
            title = post.get('title', '')
            if not title:
                title = post['content'][:100].strip()
                if '.' in title:
                    title = title.split('.')[0]
            
            # Apply subreddit-specific rules
            if subreddit == 'unpopularopinion':
                if not any(word in title.lower() for word in ['should', 'better', 'worse', 'think']):
                    title = f"{title} is overrated"  # Make it an opinion
            
            # Check if subreddit allows text posts
            if subreddit in LINK_ONLY_SUBS:
                # For link-only subs, need to provide a URL
                url = post.get('url', 'https://github.com/cruizviquez/multi-platform-blog-poster')
                submission = sub.submit(
                    title=title[:300],
                    url=url
                )
            else:
                # Text post
                submission = sub.submit(
                    title=title[:300],
                    selftext=expanded_content
                )
            
            print(f"✅ Posted to r/{subreddit}: {submission.url}")
            
            return {
                'success': True,
                'id': submission.id,
                'url': submission.url,
                'subreddit': subreddit
            }
            
        except praw.exceptions.RedditAPIException as e:
            error_msg = str(e)
            if "NO_SELFS" in error_msg or "BODY_NOT_ALLOWED" in error_msg:
                print(f"❌ r/{subreddit} doesn't allow text posts")
            return {'success': False, 'error': error_msg}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    
    
       
    def get_reddit_subreddit_rotation(self, content_type):
        """Rotate through subreddits to avoid spamming"""
        import random
    
        # Get primary subreddit for content type
        primary = Config.REDDIT_SUBREDDITS.get(content_type, 'artificial')
    
        # Sometimes use an alternative from the list
        if random.random() < 0.3:  # 30% chance to use alternative
            return random.choice(Config.REDDIT_SUBREDDIT_LIST)
    
        return primary

    
    def post_to_all(self, title, content, url):
        """Post to all configured platforms"""
        post = self.create_post(title, content, url)
        results = {}
        
        # Existing platforms (short form)
        if 'twitter' in self.platforms:
            results['twitter'] = self.post_to_twitter(post)
        
        if 'linkedin' in self.platforms:
            results['linkedin'] = self.post_to_linkedin(post)
        
        if 'facebook' in self.platforms:
            results['facebook'] = self.post_to_facebook(post)
        
        # New platforms (long form)
        if 'devto' in self.platforms:
            results['devto'] = self.post_to_devto(post)
        
        if 'medium' in self.platforms:
            results['medium'] = self.post_to_medium(post)
        
        if 'reddit' in self.platforms:
            results['reddit'] = self.post_to_reddit(post)
        
        if 'mastodon' in self.platforms:
            results['mastodon'] = self.post_to_mastodon(post)
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
        
        if 'devto' in platforms and 'devto' in self.platforms:
            results['devto'] = self.post_to_devto(post)
        
        if 'medium' in platforms and 'medium' in self.platforms:
            results['medium'] = self.post_to_medium(post)
        
        if 'reddit' in platforms and 'reddit' in self.platforms:
            results['reddit'] = self.post_to_reddit(post)
        
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
    
    def format_content_for_platform(self, platform, title, content, url):
        """Helper method to format content based on platform limits"""
        if platform == 'twitter':
            # 280 character limit
            full_text = f"{title}\n\n{content}\n\n{url}"
            if len(full_text) <= 280:
                return full_text
            else:
                # Shorten content to fit
                available = 280 - len(title) - len(url) - 10  # 10 for newlines and ...
                shortened_content = content[:available] + "..."
                return f"{title}\n\n{shortened_content}\n\n{url}"
        
        elif platform == 'linkedin':
            # LinkedIn has 3000 character limit for posts
            return f"{title}\n\n{content}\n\n{url}"
        
        elif platform == 'facebook':
            # Facebook has high limit
            return f"{title}\n\n{content}\n\n{url}"
        
        elif platform in ['devto', 'medium', 'reddit']:
            # These platforms get expanded content
            return self.expand_content_for_platform({'content': content}, platform)
        
        else:
            return f"{title}\n\n{content}\n\n{url}"