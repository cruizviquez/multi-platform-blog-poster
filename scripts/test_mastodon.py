import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mastodon import Mastodon
from config import Config

# Create client
mastodon = Mastodon(
    access_token=Config.MASTODON_ACCESS_TOKEN,
    api_base_url=Config.MASTODON_INSTANCE_URL
)

# Test connection
try:
    account = mastodon.account_verify_credentials()
    print(f"✅ Connected to Mastodon as: @{account['username']}@{account['url'].split('/')[2]}")
    
    # Test post
    status = mastodon.status_post("Hello from my automated blog poster! 🚀")
    print(f"✅ Posted! URL: {status['url']}")
except Exception as e:
    print(f"❌ Error: {e}")