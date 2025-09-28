import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import praw
from config import Config
import time

reddit = praw.Reddit(
    client_id=Config.REDDIT_CLIENT_ID,
    client_secret=Config.REDDIT_CLIENT_SECRET,
    username=Config.REDDIT_USERNAME,
    password=Config.REDDIT_PASSWORD,
    user_agent=Config.REDDIT_USER_AGENT
)

print("🔍 Testing all configured subreddits...\n")

results = {
    'no_flair_needed': [],
    'flair_required': [],
    'cannot_post': [],
    'does_not_exist': []
}

# Test each subreddit
for content_type, sub_name in Config.REDDIT_SUBREDDITS.items():
    print(f"Testing r/{sub_name} ({content_type})...")
    
    try:
        sub = reddit.subreddit(sub_name)
        
        # Check if subreddit exists
        try:
            _ = sub.subscribers
        except:
            print(f"  ❌ Subreddit doesn't exist\n")
            results['does_not_exist'].append(sub_name)
            continue
        
        # Try to check flair requirements
        try:
            # Different method to get flairs
            flairs = []
            for flair in sub.flair.link_templates:
                flairs.append(flair)
            
            print(f"  📌 Has {len(flairs)} flairs available")
            
            # Try to check post requirements
            try:
                requirements = sub.post_requirements()
                flair_required = requirements.get('flair', {}).get('required', False)
                print(f"  📋 Flair required: {flair_required}")
            except:
                print(f"  📋 Cannot check requirements")
                flair_required = None
                
        except Exception as e:
            print(f"  ⚠️  Flair check error: {e}")
            flairs = []
            flair_required = None
        
        # Test posting (without actually posting)
        try:
            # Check submission restrictions
            restricted = sub.submission_requirements()
            print(f"  🔒 Restrictions: {restricted}")
        except:
            pass
        
        # Categorize
        if flair_required == True or len(flairs) > 0:
            results['flair_required'].append(sub_name)
            print(f"  📝 Result: Might need flair\n")
        else:
            results['no_flair_needed'].append(sub_name)
            print(f"  ✅ Result: Should work without flair\n")
            
    except praw.exceptions.Forbidden:
        print(f"  ❌ Forbidden - cannot post\n")
        results['cannot_post'].append(sub_name)
    except Exception as e:
        print(f"  ❌ Error: {e}\n")
        results['cannot_post'].append(sub_name)
    
    time.sleep(1)  # Be nice to Reddit's API

# Summary
print("\n" + "="*50)
print("📊 SUMMARY")
print("="*50)

print(f"\n✅ SAFE SUBREDDITS (no flair needed): {len(results['no_flair_needed'])}")
for sub in results['no_flair_needed']:
    print(f"  - r/{sub}")

print(f"\n⚠️  NEED FLAIR: {len(results['flair_required'])}")
for sub in results['flair_required']:
    print(f"  - r/{sub}")

print(f"\n❌ CANNOT POST: {len(results['cannot_post'])}")
for sub in results['cannot_post']:
    print(f"  - r/{sub}")

print(f"\n❌ DON'T EXIST: {len(results['does_not_exist'])}")
for sub in results['does_not_exist']:
    print(f"  - r/{sub}")

# Save results
print("\n💾 Saving results to reddit_test_results.json...")
import json
with open('reddit_test_results.json', 'w') as f:
    json.dump(results, f, indent=2)