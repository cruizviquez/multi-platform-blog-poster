
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Test which model works
models_to_test = [
    "llama-3.2-1b-preview",
    "llama-3.2-3b-preview", 
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
    "gemma2-9b-it"
]

print("Testing Groq models...\n")

for model in models_to_test:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say 'Hello'"}],
            max_tokens=10
        )
        print(f"✅ {model}: WORKING")
    except Exception as e:
        print(f"❌ {model}: {str(e)[:50]}...")