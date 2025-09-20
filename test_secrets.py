import os

print("Checking secrets...")
secrets = [
    'TWITTER_API_KEY',
    'TWITTER_API_SECRET', 
    'TWITTER_ACCESS_TOKEN',
    'TWITTER_ACCESS_SECRET'
]

for secret in secrets:
    value = os.environ.get(secret)
    if value:
        print(f"✅ {secret}: Found (hidden)")
    else:
        print(f"❌ {secret}: Not found")

        