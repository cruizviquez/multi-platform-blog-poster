from expert_content_generator import ExpertContentGenerator
from social_poster import SocialMediaPoster
import json

def test_immediate_post():
    """Generate and post immediately for testing"""
    print("🧪 \n")
    
    # Generate one post
    generator = ExpertContentGenerator()
    post = generator.generate_expert_post(content_type="quick_tip")
    
    if post:
        print(f"Generated: {post['content']}\n")
        
        # Post it now
        poster = SocialMediaPoster()
        
        # For short expert posts, just use content
        results = poster.post_to_all(
            title="",
            content=post['content'],
            url=""
        )
        
        # Show results
        for platform, result in results.items():
            if result['success']:
                print(f"✅ {platform}: Posted successfully!")
            else:
                print(f"❌ {platform}: {result['error']}")
    else:
        print("❌ Failed to generate content")

if __name__ == "__main__":
    test_immediate_post()