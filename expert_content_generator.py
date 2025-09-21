import os
import json
import random
from datetime import datetime, timedelta
from groq import Groq

class ExpertContentGenerator:
    def __init__(self):
        # Remove proxy issues
        for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'proxies']:
            os.environ.pop(proxy_var, None)
        
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192"
        
        # Expert content themes
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
            "hot_take"        # Controversial opinions
        ]
        
        self.topics = [
            "neural networks", "transformers", "LLMs", "computer vision",
            "reinforcement learning", "MLOps", "AI ethics", "generative AI",
            "edge AI", "quantum ML", "federated learning", "AI in healthcare",
            "autonomous systems", "natural language processing", "AI bias",
            "explainable AI", "AI security", "multimodal AI", "AI efficiency"
        ]
    
    def generate_expert_post(self, content_type=None, topic=None):
        """Generate a single expert post"""
        if not content_type:
            content_type = random.choice(self.content_types)
        if not topic:
            topic = random.choice(self.topics)
        
        # Craft specific prompts for each content type
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
            
            "hot_take": f"Share a controversial but defensible opinion about {topic} in 200 characters. Be respectful but bold. Include 🔥"
        }
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are Carlos Ruiz Viquez, an AI/ML expert. Create engaging, authoritative content that showcases deep expertise while being accessible. Never use hashtags. Be concise and impactful."
                    },
                    {
                        "role": "user",
                        "content": prompts[content_type]
                    }
                ],
                temperature=0.8,
                max_tokens=100
            )
            
            content = response.choices[0].message.content.strip()
            
            # Ensure it's under 250 characters
            if len(content) > 250:
                content = content[:247] + "..."
            
            return {
                "content": content,
                "type": content_type,
                "topic": topic,
                "platform_suitable": ["twitter", "linkedin"],
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def generate_thread(self, topic=None, posts=3):
        """Generate a connected thread of posts"""
        if not topic:
            topic = random.choice(self.topics)
        
        thread_posts = []
        
        try:
            prompt = f"""Create a {posts}-part educational thread about {topic}.
            Each part should be under 200 characters and build on the previous.
            Format as:
            1/3: [first post]
            2/3: [second post]
            3/3: [third post]
            Make it valuable and engaging."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI/ML expert creating educational threads."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            parts = content.split('\n')
            
            for part in parts:
                if ':' in part:
                    post_content = part.split(':', 1)[1].strip()
                    if len(post_content) > 250:
                        post_content = post_content[:247] + "..."
                    
                    thread_posts.append({
                        "content": post_content,
                        "type": "thread",
                        "topic": topic,
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
        
        print(f"🤖 Generating {posts_per_day} expert posts...\n")
        
        # Ensure variety
        for i in range(posts_per_day):
            # Pick content type (avoid repeats)
            available_types = [t for t in self.content_types if t not in used_types[-3:]]
            if not available_types:
                available_types = self.content_types
            
            content_type = random.choice(available_types)
            used_types.append(content_type)
            
            # Generate post
            post = self.generate_expert_post(content_type=content_type)
            
            if post:
                daily_posts.append(post)
                print(f"✅ {content_type.upper()}: {post['content'][:50]}...")
            
            # Small delay
            import time
            time.sleep(0.5)
        
        # Add one thread
        print("\n🧵 Generating educational thread...")
        thread = self.generate_thread()
        if thread:
            daily_posts.extend(thread)
            print(f"✅ Thread created with {len(thread)} parts")
        
        return daily_posts
    
    def schedule_posts(self, posts, start_hour=9, end_hour=18):
        """Assign posting times throughout the day"""
        if not posts:
            return []
        
        # Define posting slots (avoid lunch hour)
        time_slots = [
            "09:00", "10:30", "11:45",  # Morning
            "14:00", "15:30", "17:00",  # Afternoon
            "18:30"  # Early evening
        ]
        
        scheduled_posts = []
        today = datetime.now().date()
        
        for i, post in enumerate(posts[:len(time_slots)]):
            time_slot = time_slots[i % len(time_slots)]
            hour, minute = map(int, time_slot.split(':'))
            
            scheduled_time = datetime.combine(today, datetime.min.time())
            scheduled_time = scheduled_time.replace(hour=hour, minute=minute)
            
            post['scheduled_time'] = scheduled_time.isoformat()
            post['time_slot'] = time_slot
            scheduled_posts.append(post)
        
        return scheduled_posts
    
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

# Usage script
if __name__ == "__main__":
    import sys
    
    generator = ExpertContentGenerator()
    
    if len(sys.argv) > 1 and sys.argv[1] == "thread":
        # Generate just a thread
        thread = generator.generate_thread()
        for i, post in enumerate(thread):
            print(f"\n{i+1}/{len(thread)}: {post['content']}")
    
    elif len(sys.argv) > 1 and sys.argv[1] == "preview":
        # Preview different types
        for content_type in ["breakthrough", "myth_buster", "quick_tip", "question"]:
            post = generator.generate_expert_post(content_type=content_type)
            if post:
                print(f"\n{content_type.upper()}:")
                print(post['content'])
    
    else:
        # Generate daily content
        daily_posts = generator.generate_daily_content(posts_per_day=6)
        
        # Schedule them
        scheduled = generator.schedule_posts(daily_posts)
        
        # Save to queue
        generator.save_to_expert_queue(scheduled)
        
        print("\n📅 Posting Schedule:")
        for post in scheduled:
            print(f"{post['time_slot']} - {post['type']}: {post['content'][:60]}...")
