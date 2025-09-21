from social_poster import SocialMediaPoster
import json
import sys

def post_from_queue():
    """Post the next item from content queue"""
    poster = SocialMediaPoster()
    
    # Load content queue
    try:
        with open('content_queue.json', 'r') as f:
            posts = json.load(f)
    except FileNotFoundError:
        print("❌ content_queue.json not found!")
        return
    except json.JSONDecodeError:
        print("❌ content_queue.json is not valid JSON!")
        return
    
    if not posts:
        print("📭 No posts in queue!")
        return
    
    # Get the first post
    next_post = posts[0]
    
    print(f"📤 Posting: {next_post['title']}")
    
    # Post to all platforms
    results = poster.post_to_all(
        title=next_post['title'],
        content=next_post['content'],
        url=next_post['url']
    )
    
    # Show results
    all_success = True
    for platform, result in results.items():
        if result['success']:
            print(f"✅ {platform}: Posted successfully!")
        else:
            print(f"❌ {platform}: {result['error']}")
            all_success = False
    
    # If posted successfully, remove from queue
    if all_success:
        posts.pop(0)
        with open('content_queue.json', 'w') as f:
            json.dump(posts, f, indent=2)
        print(f"✅ Removed from queue. {len(posts)} posts remaining.")
    else:
        print("⚠️  Post kept in queue due to errors.")

def post_single(title, content, url):
    """Post a single item directly"""
    poster = SocialMediaPoster()
    
    print(f"📤 Direct posting: {title}")
    
    results = poster.post_to_all(title=title, content=content, url=url)
    
    for platform, result in results.items():
        if result['success']:
            print(f"✅ {platform}: Posted successfully!")
        else:
            print(f"❌ {platform}: {result['error']}")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "queue":
            post_from_queue()
        elif sys.argv[1] == "test":
            # Test post
            post_single(
                "Post",
                "My multi-platform poster",
                "https://carlosruizviquezinformationtechnology.blogspot.com/2025/09/about-dr-carlos-ruiz-viquez.html"
            )
    else:
        # Default: post from queue
        post_from_queue()

if __name__ == "__main__":
    main()