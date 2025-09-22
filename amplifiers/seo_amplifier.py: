import os
import json
import requests
from datetime import datetime
from groq import Groq
import time

class SEOAmplifier:
    def __init__(self):
        # Remove proxy issues
        for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'proxies']:
            os.environ.pop(proxy_var, None)
        
        # Initialize Groq for content expansion
        self.groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.1-70b-versatile"  # Best for longer content
        
        # Platform credentials
        self.devto_api_key = os.environ.get("DEVTO_API_KEY")
        self.medium_token = os.environ.get("MEDIUM_ACCESS_TOKEN")
        self.medium_user_id = os.environ.get("MEDIUM_USER_ID")
        
        # Track published articles to avoid duplicates
        self.published_history = self.load_published_history()
    
    def load_published_history(self):
        """Load history of published articles"""
        try:
            with open('published_articles.json', 'r') as f:
                return json.load(f)
        except:
            return {"articles": []}
    
    def save_published_history(self):
        """Save published history"""
        with open('published_articles.json', 'w') as f:
            json.dump(self.published_history, f, indent=2)
    
    def expand_expert_post(self, expert_post):
        """Expand a 250-char expert post into a full article"""
        print(f"\n📝 Expanding: {expert_post['content'][:60]}...")
        
        try:
            # Create expansion prompt based on post type
            expansion_prompts = {
                "quick_tip": "Expand this ML tip into a practical tutorial with code examples:",
                "breakthrough": "Expand this AI breakthrough into an article explaining its significance and applications:",
                "myth_buster": "Expand this myth-busting point into an educational article with evidence:",
                "case_study": "Expand this case study into a detailed success story with metrics:",
                "tutorial": "Expand this concept into a beginner-friendly tutorial with examples:",
                "prediction": "Expand this prediction into an analysis with supporting trends:",
                "tool_review": "Expand this tool review into a comprehensive guide with use cases:",
                "challenge": "Expand this challenge into an article exploring solutions:",
                "comparison": "Expand this comparison into a detailed analysis with pros/cons:",
                "warning": "Expand this warning into a guide on avoiding common pitfalls:"
            }
            
            prompt_type = expansion_prompts.get(expert_post.get('type'), 
                                               "Expand this into an informative article:")
            
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are Carlos Ruiz Viquez, an AI/ML expert writing for Medium and Dev.to. 
                        Create engaging, SEO-friendly articles that provide real value. Include:
                        - A compelling introduction
                        - Clear sections with subheadings
                        - Practical examples or code when relevant
                        - Key takeaways or conclusions
                        - Aim for 800-1200 words
                        - Use markdown formatting
                        - Include relevant keywords naturally
                        - Make it actionable and valuable"""
                    },
                    {
                        "role": "user",
                        "content": f"{prompt_type}\n\nOriginal: {expert_post['content']}\n\nTopic: {expert_post.get('topic', 'AI/ML')}"
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            expanded_content = response.choices[0].message.content
            
            # Generate SEO-friendly title
            title_response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Create an SEO-friendly, compelling article title (max 60 chars) that would rank well on Google."
                    },
                    {
                        "role": "user",
                        "content": f"Create a title for this article about: {expert_post['content']}"
                    }
                ],
                temperature=0.8,
                max_tokens=30
            )
            
            title = title_response.choices[0].message.content.strip().strip('"')
            
            # Generate meta description
            meta_response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Write a compelling meta description (150-160 chars) for SEO."
                    },
                    {
                        "role": "user",
                        "content": f"Meta description for: {expanded_content[:300]}..."
                    }
                ],
                temperature=0.7,
                max_tokens=50
            )
            
            meta_description = meta_response.choices[0].message.content.strip()
            
            # Generate tags
            tags = self.generate_tags(expert_post.get('topic', ''), expert_post.get('type', ''))
            
            return {
                "title": title,
                "content": expanded_content,
                "meta_description": meta_description,
                "tags": tags,
                "original_post": expert_post['content'],
                "post_type": expert_post.get('type', 'article'),
                "topic": expert_post.get('topic', 'AI/ML')
            }
            
        except Exception as e:
            print(f"❌ Error expanding post: {e}")
            return None
    
    def generate_tags(self, topic, post_type):
        """Generate relevant tags for the article"""
        base_tags = ["artificialintelligence", "machinelearning", "ai", "technology"]
        
        topic_tags = {
            "neural networks": ["deeplearning", "neuralnetworks"],
            "transformers": ["nlp", "transformers", "llm"],
            "computer vision": ["computervision", "imageprocessing"],
            "mlops": ["mlops", "devops", "deployment"],
            "generative AI": ["generativeai", "aigc", "chatgpt"],
            "ai ethics": ["aiethics", "responsibleai"],
            "llms": ["llm", "largelanguagemodels", "gpt"]
        }
        
        # Add topic-specific tags
        for key, tags in topic_tags.items():
            if key.lower() in topic.lower():
                base_tags.extend(tags)
                break
        
        # Add post-type tags
        if post_type == "tutorial":
            base_tags.extend(["tutorial", "howto"])
        elif post_type == "case_study":
            base_tags.extend(["casestudy", "realworld"])
        
        # Return unique tags
        return list(set(base_tags))[:5]  # Most platforms limit tags
    
    def post_to_devto(self, article):
        """Post article to Dev.to"""
        if not self.devto_api_key:
            print("❌ Dev.to API key not configured")
            return None
        
        headers = {
            'api-key': self.devto_api_key,
            'Content-Type': 'application/json'
        }
        
        # Format content for Dev.to
        devto_content = f"""
{article['content']}

---

*Originally posted as an AI/ML insight. Follow me for more expert content on artificial intelligence and machine learning.*

**Key Topics**: {', '.join(article['tags'])}
"""
        
        article_data = {
            'article': {
                'title': article['title'],
                'body_markdown': devto_content,
                'tags': article['tags'][:4],  # Dev.to allows max 4 tags
                'published': True,
                'description': article['meta_description']
            }
        }
        
        try:
            response = requests.post(
                'https://dev.to/api/articles',
                headers=headers,
                json=article_data
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Published to Dev.to: {result['url']}")
                return {
                    'platform': 'devto',
                    'url': result['url'],
                    'id': result['id']
                }
            else:
                print(f"❌ Dev.to error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Dev.to posting error: {e}")
            return None
    
    def post_to_medium(self, article):
        """Post article to Medium"""
        if not self.medium_token or not self.medium_user_id:
            print("❌ Medium credentials not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.medium_token}',
            'Content-Type': 'application/json'
        }
        
        # Format for Medium
        medium_content = f"""
# {article['title']}

{article['content']}

---

*Follow me for more AI/ML insights and tutorials.*
"""
        
        article_data = {
            'title': article['title'],
            'contentFormat': 'markdown',
            'content': medium_content,
            'tags': article['tags'][:5],  # Medium allows max 5 tags
            'publishStatus': 'public'
        }
        
        try:
            response = requests.post(
                f'https://api.medium.com/v1/users/{self.medium_user_id}/posts',
                headers=headers,
                json=article_data
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Published to Medium: {result['data']['url']}")
                return {
                    'platform': 'medium',
                    'url': result['data']['url'],
                    'id': result['data']['id']
                }
            else:
                print(f"❌ Medium error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Medium posting error: {e}")
            return None
    
    def amplify_expert_posts(self, num_posts=1):
        """Load expert posts and amplify them to articles"""
        # Load expert queue
        try:
            with open('expert_queue.json', 'r') as f:
                expert_posts = json.load(f)
        except:
            print("❌ No expert posts found in queue")
            return
        
        if not expert_posts:
            print("📭 Expert queue is empty")
            return
        
        # Process specified number of posts
        amplified_count = 0
        for i in range(min(num_posts, len(expert_posts))):
            post = expert_posts[i]
            
            # Check if already published
            if self.is_already_published(post['content']):
                print(f"⏭️  Skipping already published: {post['content'][:50]}...")
                continue
            
            # Expand the post
            article = self.expand_expert_post(post)
            
            if article:
                # Post to platforms
                results = []
                
                # Post to Dev.to
                devto_result = self.post_to_devto(article)
                if devto_result:
                    results.append(devto_result)
                
                # Small delay between platforms
                time.sleep(2)
                
                # Post to Medium
                medium_result = self.post_to_medium(article)
                if medium_result:
                    results.append(medium_result)
                
                # Track publication
                if results:
                    self.track_publication(post, article, results)
                    amplified_count += 1
                
                # Delay between posts
                time.sleep(5)
        
        print(f"\n📊 Amplified {amplified_count} posts to SEO platforms")
    
    def is_already_published(self, content):
        """Check if content was already published"""
        content_start = content[:50].lower()
        for article in self.published_history['articles']:
            if article['original_content'][:50].lower() == content_start:
                return True
        return False
    
    def track_publication(self, original_post, article, results):
        """Track published articles"""
        publication_record = {
            'original_content': original_post['content'],
            'title': article['title'],
            'published_at': datetime.now().isoformat(),
            'platforms': results,
            'topic': article['topic'],
            'type': article['post_type']
        }
        
        self.published_history['articles'].append(publication_record)
        self.save_published_history()
# Add this to the end of seo_amplifier.py after the main execution line

    import sys
    
    amplifier = SEOAmplifier()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--post":
            # Amplify and post
            amplifier.amplify_expert_posts(num_posts=3)
        elif sys.argv[1] == "--preview":
            # Just preview expansion
            with open('expert_queue.json', 'r') as f:
                posts = json.load(f)
            if posts:
                article = amplifier.expand_expert_post(posts[0])
                if article:
                    print(f"\n📄 Title: {article['title']}")
                    print(f"\n📝 Preview:\n{article['content'][:500]}...")
                    print(f"\n🏷️ Tags: {', '.join(article['tags'])}")
        else:
            try:
                num = int(sys.argv[1])
                amplifier.amplify_expert_posts(num_posts=num)
            except:
                print("Usage: python seo_amplifier.py [--post|--preview|number]")
    else:
        # Default: amplify 1 post
        amplifier.amplify_expert_posts(num_posts=1)