import os
import json
import random
from datetime import datetime

# Handle proxy issues in Codespaces
for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'proxies']:
    os.environ.pop(proxy_var, None)

# Now import Groq
from groq import Groq

class AIContentGenerator:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        self.client = Groq(api_key=api_key)
        
        # Use current available model
        self.model = "llama-3.1-8b-instant"  # Updated model name
        
        # Your blog focus areas
        self.topics = [
            "Python programming tricks",
            "Machine Learning applications",
            "Web Development best practices",
            "Data Science projects",
            "AI and automation",
            "Cloud Computing solutions",
            "Cybersecurity for developers",
            "API design patterns",
            "Database optimization",
            "DevOps workflows"
        ]
        
        self.base_url = "https://carlosruizviquezinformationtechnology.blogspot.com/"





        
    def generate_single_post(self, topic=None):
        """Generate one blog post idea"""
        if not topic:
            topic = random.choice(self.topics)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are Carlos Ruiz Viquez, a technology expert and blogger. Generate creative, engaging blog post ideas that haven't been overdone."
                    },
                    {
                        "role": "user",
                        "content": f"""Generate a unique blog post idea about {topic}.
                        
                        Format your response EXACTLY like this:
                        TITLE: [Catchy, specific title]
                        DESCRIPTION: [2-3 sentences that make people want to read more]
                        KEYWORDS: [3-5 relevant keywords separated by commas]
                        """
                    }
                ],
                temperature=0.8,  # High creativity
                max_tokens=300
            )
            
            # Parse the response
            content = response.choices[0].message.content
            lines = content.strip().split('\n')
            
            title = ""
            description = ""
            keywords = ""
            
            for line in lines:
                if line.startswith("TITLE:"):
                    title = line.replace("TITLE:", "").strip()
                elif line.startswith("DESCRIPTION:"):
                    description = line.replace("DESCRIPTION:", "").strip()
                elif line.startswith("KEYWORDS:"):
                    keywords = line.replace("KEYWORDS:", "").strip()
            
            # Generate URL slug
            url_slug = title.lower()
            url_slug = ''.join(c if c.isalnum() or c == ' ' else '' for c in url_slug)
            url_slug = url_slug.replace(' ', '-')[:50]
            
            return {
                "title": title,
                "content": description,
                "url": f"{self.base_url}2024/{url_slug}",
                "keywords": keywords,
                "generated_by": "AI",
                "generated_at": datetime.now().isoformat(),
                "topic": topic
            }
            
        except Exception as e:
            print(f"❌ Error generating content: {e}")
            return None
    
    def generate_week_of_content(self):
        """Generate 7 posts (one for each day)"""
        posts = []
        used_topics = []
        
        print("🤖 Generating a week of content...")
        
        for i in range(7):
            # Ensure variety in topics
            available_topics = [t for t in self.topics if t not in used_topics]
            if not available_topics:
                available_topics = self.topics
                used_topics = []
            
            topic = random.choice(available_topics)
            used_topics.append(topic)
            
            post = self.generate_single_post(topic)
            if post:
                posts.append(post)
                print(f"✅ Generated: {post['title']}")
            
            # Small delay to respect rate limits
            import time
            time.sleep(1)
        
        return posts
    
    def add_to_queue(self, posts):
        """Add posts to content_queue.json"""
        try:
            with open('content_queue.json', 'r') as f:
                queue = json.load(f)
        except:
            queue = []
        
        # Add new posts
        queue.extend(posts)
        
        # Save back
        with open('content_queue.json', 'w') as f:
            json.dump(queue, f, indent=2)
        
        print(f"\n✅ Added {len(posts)} posts to queue")
        print(f"📋 Total posts in queue: {len(queue)}")
    
    def preview_generation(self, count=3):
        """Preview what AI will generate"""
        print(f"\n🔍 Previewing {count} AI-generated posts:\n")
        
        for i in range(count):
            post = self.generate_single_post()
            if post:
                print(f"Post {i+1}:")
                print(f"📌 Title: {post['title']}")
                print(f"📝 Description: {post['content']}")
                print(f"🏷️  Keywords: {post['keywords']}")
                print(f"🔗 URL: {post['url']}")
                print("-" * 50)