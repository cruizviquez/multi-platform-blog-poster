# generate_content.py
from groq_generator import AIContentGenerator
import sys
import json

def show_queue_status():
    """Display current queue status"""
    try:
        with open('content_queue.json', 'r') as f:
            queue = json.load(f)
        print(f"\n📋 Current queue has {len(queue)} posts")
    except:
        print("\n📋 Queue is empty or not found")

def main():
    # Check if API key exists
    import os
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment variables")
        print("Please add it to GitHub Secrets and restart Codespace")
        return
    
    # Create generator instance
    try:
        generator = AIContentGenerator()
    except Exception as e:
        print(f"❌ Error creating generator: {e}")
        return
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "preview":
            # Preview AI generation without saving
            print("🔍 Preview mode - won't save to queue\n")
            generator.preview_generation(count=3)
        
        elif command == "week":
            # Generate a full week of content
            print("📅 Generating a week of content...")
            posts = generator.generate_week_of_content()
            if posts:
                generator.add_to_queue(posts)
                show_queue_status()
            else:
                print("❌ No posts were generated")
        
        elif command == "single":
            # Generate just one post
            print("📝 Generating a single post...")
            post = generator.generate_single_post()
            if post:
                generator.add_to_queue([post])
                print(f"\n✅ Generated: {post['title']}")
                show_queue_status()
            else:
                print("❌ Failed to generate post")
        
        elif command == "status":
            # Just show queue status
            show_queue_status()
            try:
                with open('content_queue.json', 'r') as f:
                    queue = json.load(f)
                if queue:
                    print("\nNext 3 posts:")
                    for i, post in enumerate(queue[:3]):
                        print(f"{i+1}. {post.get('title', 'No title')}")
            except:
                pass
        
        elif command == "help":
            # Show help
            print("\n📚 AI Content Generator - Commands:")
            print("\nUsage: python generate_content.py [command]\n")
            print("Commands:")
            print("  preview  - Preview 3 AI-generated posts (no saving)")
            print("  single   - Generate and queue 1 post")
            print("  week     - Generate and queue 7 posts")
            print("  status   - Show current queue status")
            print("  help     - Show this help message")
            print("\nNo command - Generate and queue 3 posts (default)")
        
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'python generate_content.py help' for available commands")
    
    else:
        # Default behavior: generate 3 posts
        print("🤖 Generating 3 blog posts...")
        posts = []
        
        for i in range(3):
            print(f"\nGenerating post {i+1}/3...")
            post = generator.generate_single_post()
            if post:
                posts.append(post)
                print(f"✅ Created: {post['title']}")
            else:
                print(f"❌ Failed to generate post {i+1}")
        
        if posts:
            generator.add_to_queue(posts)
            show_queue_status()
        else:
            print("\n❌ No posts were generated successfully")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()