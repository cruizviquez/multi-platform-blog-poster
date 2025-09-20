from social_poster import SocialMediaPoster

print("🚀 Testing Blog Poster...")

# Initialize
poster = SocialMediaPoster()

# Test post
results = poster.post_to_all(
    title="Testing My Blog Automation",
    content="This is my automated content distribution system working!",
    url="https://github.com/cruizviquez/multi-platform-blog-poster"
)

if results.get('twitter', {}).get('success'):
    print("✅ Tweet posted successfully!")
    print(f"Tweet ID: {results['twitter']['id']}")
else:
    print("❌ Failed:", results.get('twitter', {}).get('error'))