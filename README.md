# Multi-Platform Blog Poster

Automate your blog content distribution across multiple social media platforms with a single tool. Write once, publish everywhere.

## ✨ Features

- 📝 Post to multiple platforms simultaneously
- 📅 Schedule posts in advance
- 📊 Track post performance
- 🔄 Content queue management
- 🛡️ Platform API rate limit handling

## 🚀 Quick Start

### Using GitHub Codespaces

1. Click the green "Code" button above
2. Select "Create codespace on main"
3. Wait for the environment to load
4. Run the setup commands below

### Local Development

# Clone the repository
git clone https://github.com/yourusername/multi-platform-blog-poster.git
cd multi-platform-blog-poster

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API credentials

### ⚙️ Configuration

    Copy .env.example to .env
    Add your API credentials:

env

# Twitter/X
TWITTER_API_KEY=your_key_here
TWITTER_API_SECRET=your_secret_here
TWITTER_ACCESS_TOKEN=your_token_here
TWITTER_ACCESS_SECRET=your_token_secret_here

# Add other platforms as needed

📖 Usage
Basic Usage

python

from social_poster import SocialMediaPoster

poster = SocialMediaPoster()
results = poster.post_to_all(
    title="My New Blog Post",
    content="Check out my latest article about Python...",
    url="https://myblog.com/new-post"
)

Scheduled Posting

bash

# Run the scheduler
python scheduler.py

Content Queue

Add posts to content_queue.json:

json

[
    {
        "title": "Blog Post Title",
        "content": "Post description...",
        "url": "https://yourblog.com/post"
    }
]

🔧 Supported Platforms

    ✅ Twitter/X
    🔄 LinkedIn (coming soon)
    🔄 Facebook Pages (coming soon)
    🔄 Instagram (coming soon)
    🔄 Mastodon (coming soon)

📁 Project Structure

text

multi-platform-blog-poster/
├── .env.example          # Environment variables template
├── requirements.txt      # Python dependencies
├── config.py            # Configuration management
├── social_poster.py     # Main posting logic
├── scheduler.py         # Post scheduling
├── main.py             # Entry point
├── content_queue.json   # Scheduled posts
└── logs/               # Posting logs

### 🤝 Contributing

    Fork the repository
    Create your feature branch (git checkout -b feature/amazing-feature)
    Commit your changes (git commit -m 'Add amazing feature')
    Push to the branch (git push origin feature/amazing-feature)
    Open a Pull Request

### ⚠️ Important Notes

    Always respect platform API rate limits
    Follow each platform's terms of service
    Use responsibly - avoid spam
    Keep your API credentials secure

### 📝 License

MIT License - see LICENSE file for details

### 🆘 Support

    Create an issue for bug reports
    Check existing issues before creating new ones
    Star ⭐ the repo if you find it helpful!

Built with ❤️ for content creators who value their time (By. Dr. Carlos Ruiz Viquez)

text


### **.env.example:**
```env
# Twitter/X API Credentials
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=

# LinkedIn API Credentials
LINKEDIN_ACCESS_TOKEN=

# Facebook API Credentials
FACEBOOK_PAGE_ID=
FACEBOOK_ACCESS_TOKEN=

# Posting Schedule (24-hour format)
POST_TIMES=09:00,15:00,19:00

# Timezone
TIMEZONE=UTC




