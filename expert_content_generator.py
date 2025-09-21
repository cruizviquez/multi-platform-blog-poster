# expert_content_generator.py
import os
import json
import random
import hashlib
from datetime import datetime, timedelta
from groq import Groq

class ExpertContentGenerator:
    def __init__(self):
        # Remove proxy issues
        for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'proxies']:
            os.environ.pop(proxy_var, None)
        
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"  # Updated to working model
        
        # Load post history to avoid duplicates
        self.post_history = self.load_post_history()
        
        # Expert content themes - ALL must have matching prompts
        self.content_types = [
            "breakthrough",    # Latest AI breakthroughs
            "myth_buster",    # Debunk AI myths
            "quick_tip",      # Practical ML tips
            "did_you_know",   # Interesting facts
            "prediction",     # Future trends
            "case_study",     # Real-world applications
            "tutorial",       # Mini tutorials
            "thought_leader", # Industry insights
            "question",       # Engaging questions
            "hot_take",       # Controversial opinions
            "code_snippet",   # Quick code examples
            "paper_insight",  # Latest research papers
            "tool_review",    # AI tool recommendations
            "challenge",      # Technical challenges
            "comparison",     # Compare AI approaches
            "warning",        # Common pitfalls
            "success_metric", # KPIs and metrics
        ]
        
        self.topics = [
            "neural networks", "transformers", "LLMs", "computer vision",
            "reinforcement learning", "MLOps", "AI ethics", "generative AI",
            "edge AI", "quantum ML", "federated learning", "AI in healthcare",
            "autonomous systems", "natural language processing", "AI bias",
            "explainable AI", "AI in Cybersecurity", "multimodal AI", "AI efficiency",
            "prompt engineering", "AI agents", "RAG systems", "fine-tuning LLMs",
            "AI governance", "synthetic data", "AI sustainability", "distributed training",
            "AI agents","AI in Adverstisement", "AI in Media", "AI Sports Coach","AI in Netflix"
        ]
        
        self.base_url = "https://carlosruizviquezinformationtechnology.blogspot.com/"
    
    def load_post_history(self):
        """Load history of generated posts to avoid duplicates"""
        try:
            with open('post_history_expert.json', 'r') as f:
                return json.load(f)
        except:
            return {"hashes": [], "posts": []}
    
    def save_post_history(self):
        """Save post history"""
        # Keep only last 1000 posts to prevent file from growing too large
        if len(self.post_history["hashes"]) > 1000:
            self.post_history["hashes"] = self.post_history["hashes"][-1000:]
            self.post_history["posts"] = self.post_history["posts"][-1000:]
        
        with open('post_history_expert.json', 'w') as f:
            json.dump(self.post_history, f, indent=2)
    
    def is_duplicate(self, content):
        """Check if content is too similar to previous posts"""
        # Create hash of content
        content_hash = hashlib.md5(content.lower().encode()).hexdigest()
        
        # Check exact match
        if content_hash in self.post_history["hashes"]:
            return True
        
        # Check similarity (first 50 chars)
        content_start = content[:50].lower()
        for post in self.post_history["posts"][-100:]:  # Check last 100 posts
            if post.get("content", "")[:50].lower() == content_start:
                return True
        
        return False
    
    def generate_expert_post(self, content_type=None, topic=None, retry_count=0):
        """Generate a single expert post with duplicate checking"""
        if retry_count > 3:
            print("⚠️ Max retries reached, returning None")
            return None
        
        if not content_type:
            content_type = random.choice(self.content_types)
        if not topic:
            topic = random.choice(self.topics)
        
        # Complete prompts dictionary - MUST match content_types list
        prompts = {
            "breakthrough": f"Share a recent breakthrough in {topic} in 200 characters. Make it exciting and accessible. Include 🚀",
            
            "myth_buster": f"Bust a common myth about {topic} in 200 characters. Start with 'Myth:' then 'Reality:'. Be educational.",
            
            "quick_tip": f"Share a practical tip about {topic} for ML practitioners in 200 characters. Make it actionable. Include 💡",
            
            "did_you_know": f"Share a fascinating fact about {topic} in 200 characters. Start with 'Did you know'. Make it surprising.",
            
            "prediction": f"Make a bold prediction about {topic} for the next 2 years in 200 characters. Be specific. Include 🔮",
            
            "case_study": f"Share a real-world success story using {topic} in 200 characters. Include concrete results. Use 📊",
            
            "tutorial": f"Explain one concept about {topic} in 200 characters. Make it beginner-friendly. Include 🎓",
            
            "thought_leader": f"Share an industry insight about {topic} in 200 characters. Be authoritative and forward-thinking.",
            
            "question": f"Ask an engaging question about {topic} that sparks discussion in 200 characters. Make experts want to answer.",
            
            "hot_take": f"Share a controversial but defensible opinion about {topic} in 200 characters. Be respectful but bold. Include 🔥",
            
            "code_snippet": f"Share a powerful 3-line {topic} code snippet with explanation in 200 chars. Make it practical and runnable.",
            
            "paper_insight": f"Share a key finding from recent {topic} research in 200 chars. Cite the impact, not the paper. Include 📚",
            
            "tool_review": f"Recommend an underrated {topic} tool/library in 200 chars. Include specific use case. Add ⚡",
            
            "challenge": f"Pose a technical {topic} challenge for the community in 200 chars. Make experts think. Use 🧩",
            
            "comparison": f"Compare two {topic} approaches in 200 chars. Be fair but have a clear preference. Use VS.",
            
            "warning": f"Warn about a common {topic} mistake in 200 chars. Include the fix. Use ⚠️",
            
            "success_metric": f"Share a key metric for measuring {topic} success in 200 chars. Be specific with numbers. Use 📈"
        }
        
        try:
            # Add randomness to avoid repetition
            creativity = 0.8 + (random.random() * 0.2)  # 0.8 to 1.0
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are Dr. Carlos Ruiz Viquez, a PhD in AI/ML expert. Create engaging, authoritative content that showcases deep expertise while being accessible. Never use hashtags. Be concise and impactful. Current date: {datetime.now().strftime('%B %Y')}. Make each post unique and fresh."
                    },
                    {
                        "role": "user",
                        "content": prompts[content_type] + f" Make it unique and different from typical {topic} posts."
                    }
                ],
                temperature=creativity,
                max_tokens=150
            )
            
            content = response.choices[0].message.content.strip()
            
            # Ensure it's under 250 characters
            if len(content) > 250:
                content = content[:247] + "..."
            
            # Check for duplicates
            if self.is_duplicate(content):
                print(f"🔄 Duplicate detected, regenerating...")
                return self.generate_expert_post(content_type, None, retry_count + 1)  # Try different topic
            
            # Add to history
            content_hash = hashlib.md5(content.lower().encode()).hexdigest()
            self.post_history["hashes"].append(content_hash)
            
            post_data = {
                "content": content,
                "type": content_type,
                "topic": topic,
                "hash": content_hash,
                "platform_suitable": ["twitter", "linkedin"],
                "generated_at": datetime.now().isoformat()
            }
            
            self.post_history["posts"].append(post_data)
            self.save_post_history()
            
            return post_data
            
        except Exception as e:
            print(f"❌ Error generating content: {e}")
            return None
    
    def generate_thread(self, topic=None, posts=3):
        """Generate a connected thread of posts"""
        if not topic:
            topic = random.choice(self.topics)
        
        thread_posts = []
        
        try:
            prompt = f"""Create a {posts}-part educational thread about {topic}.
            Each part should be under 200 characters and build on the previous.
            Make it unique and not generic. Include specific examples or numbers.
            Format as:
            1/{posts}: [first post]
            2/{posts}: [second post]
            3/{posts}: [third post]
            Make each part valuable on its own but better together."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are Dr. Carlos Ruiz Viquez a PhD in AI/ML expert creating educational threads. Be specific and unique."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            parts = content.split('\n')
            
            for i, part in enumerate(parts):
                if ':' in part and f"{i+1}/{posts}" in part:
                    post_content = part.split(':', 1)[1].strip()
                    if len(post_content) > 250:
                        post_content = post_content[:247] + "..."
                    
                    thread_posts.append({
                        "content": post_content,
                        "type": "thread",
                        "topic": topic,
                        "thread_position": f"{i+1}/{posts}",
                        "platform_suitable": ["twitter", "linkedin"],
                        "generated_at": datetime.now().isoformat()
                    })
            
            return thread_posts
            
        except Exception as e:
            print(f"❌ Thread generation error: {e}")
            return []
    
    def generate_daily_content(self, posts_per_day=6):
        """Generate a day's worth of varied content"""
        daily_posts = []
        used_types = []
        used_topics = []
        
        print(f"🤖 Generating {posts_per_day} expert posts...\n")
        
        # Ensure variety
        for i in range(posts_per_day):
            # Pick content type (avoid recent repeats)
            available_types = [t for t in self.content_types if t not in used_types[-3:]]
            if not available_types:
                available_types = self.content_types
                used_types = []
            
            content_type = random.choice(available_types)
            used_types.append(content_type)
            
            # Pick topic (avoid recent repeats)
            available_topics = [t for t in self.topics if t not in used_topics[-2:]]
            if not available_topics:
                available_topics = self.topics
                used_topics = []
            
            topic = random.choice(available_topics)
            used_topics.append(topic)
            
            # Generate post
            post = self.generate_expert_post(content_type=content_type, topic=topic)
            
            if post:
                daily_posts.append(post)
                print(f"✅ {content_type.upper()}: {post['content'][:60]}...")
            
            # Small delay to respect rate limits
            import time
            time.sleep(0.5)
        
        # Add one thread
        print("\n🧵 Generating educational thread...")
        thread = self.generate_thread()
        if thread:
            daily_posts.extend(thread)
            print(f"✅ Thread created with {len(thread)} parts")
        
        return daily_posts
    
    def prepare_posts(self, posts):
        """Prepare posts without time scheduling (simplified version)"""
        if not posts:
            return []
        
        # Just add order information
        for i, post in enumerate(posts):
            post['queue_position'] = i + 1
            post['added_to_queue'] = datetime.now().isoformat()
        
        return posts
    
    def save_to_expert_queue(self, posts):
        """Save to a separate expert content queue"""
        try:
            with open('expert_queue.json', 'r') as f:
                queue = json.load(f)
        except:
            queue = []
        
        queue.extend(posts)
        
        with open('expert_queue.json', 'w') as f:
            json.dump(queue, f, indent=2)
        
        print(f"\n✅ Saved {len(posts)} posts to expert_queue.json")
        print(f"📋 Total in queue: {len(queue)}")
    
    def preview_generation(self, count=3):
        """Preview what AI will generate"""
        print(f"\n🔍 Previewing {count} AI-generated posts:\n")
        
        for i in range(count):
            # Use different content types for preview
            content_type = self.content_types[i % len(self.content_types)]
            post = self.generate_expert_post(content_type=content_type)
            
            if post:
                print(f"Post {i+1} ({post['type']}):")
                print(f"📌 Topic: {post['topic']}")
                print(f"📝 Content: {post['content']}")
                print("-" * 60)
    
    def get_queue_status(self):
        """Get current queue status"""
        try:
            with open('expert_queue.json', 'r') as f:
                queue = json.load(f)
            return len(queue)
        except:
            return 0
    
    def clear_queue(self):
        """Clear the expert queue"""
        with open('expert_queue.json', 'w') as f:
            json.dump([], f)
        print("🗑️ Expert queue cleared")

# Main execution
if __name__ == "__main__":
    import sys
    
    generator = ExpertContentGenerator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "thread":
            # Generate just a thread
            thread = generator.generate_thread()
            for i, post in enumerate(thread):
                print(f"\n{post.get('thread_position', f'{i+1}/3')}: {post['content']}")
        
        elif command == "preview":
            # Preview different types
            generator.preview_generation(count=4)
        
        elif command == "week":
            # Generate a week of content
            all_posts = []
            for day in range(7):
                print(f"\n📅 Generating content for Day {day+1}...")
                daily = generator.generate_daily_content(posts_per_day=5)
                all_posts.extend(daily)
            
            generator.save_to_expert_queue(all_posts)
            print(f"\n🎉 Generated {len(all_posts)} posts for the week!")
        
        elif command == "status":
            # Check queue status
            count = generator.get_queue_status()
            print(f"📋 Expert queue has {count} posts")
            
            if count > 0:
                with open('expert_queue.json', 'r') as f:
                    queue = json.load(f)
                print("\nNext 3 posts:")
                for i, post in enumerate(queue[:3]):
                    print(f"{i+1}. {post['content'][:80]}...")
        
        elif command == "clear":
            # Clear the queue
            response = input("⚠️  Clear entire expert queue? (yes/no): ")
            if response.lower() == "yes":
                generator.clear_queue()
        
        else:
            print(f"❌ Unknown command: {command}")
            print("\nAvailable commands:")
            print("  preview - Preview generated content")
            print("  thread  - Generate a single thread")
            print("  week    - Generate a week of content")
            print("  status  - Check queue status")
            print("  clear   - Clear the queue")
            print("\nNo command = Generate daily content")
    
    else:
        # Default: generate daily content
        daily_posts = generator.generate_daily_content(posts_per_day=6)
        
        # Prepare them (no scheduling)
        prepared = generator.prepare_posts(daily_posts)
        
        # Save to queue
        generator.save_to_expert_queue(prepared)
        
        print(f"\n✅ Added {len(prepared)} posts to queue")
        print("📋 Posts will be shared every 30 minutes by the interval poster")
        print("\nTo post them, run: python simple_interval_poster.py")