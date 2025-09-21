# Multi-Platform Blog Poster

Automated content distribution system for blog posts and AI/ML expert insights across social media platforms with SEO optimization.

## 🚀 Features

- **Multi-Platform Posting**: Twitter/X, LinkedIn, Facebook (Medium & Dev.to coming)
- **AI Content Generation**: Blog posts and expert insights using Groq AI
- **SEO Amplification**: Convert short posts into full articles
- **Flexible Scheduling**: Post at intervals or specific times
- **Duplicate Prevention**: Track posting history

## 📦 Quick Start

1. **Clone & Install**

git clone https://github.com/cruizviquez/multi-platform-blog-poster.git
cd multi-platform-blog-poster
pip install -r requirements.txt

2.- ** Configure (use .env for local testing or GitHub Secrets for Codespaces)**:
cp .env.example .env


# Add your API credentials

3.-  ** Generate Content: **

# Generate expert posts
python expert_content_generator.py

# Preview without saving
python expert_content_generator.py preview

# Generate a week of content
python expert_content_generator.py week

4.-  **  Post Content: **

# Post from queue
python main.py

# Post every 30 minutes
python simple_interval_poster.py

# Post every hour
python simple_interval_poster.py 60

5.-   ** SEO Amplification: **


# Expand posts to articles (when configured)
python seo_amplifier.py

📁 File Structure

    config.py - API credentials management
    social_poster.py - Core posting logic for all platforms
    expert_content_generator.py - Generates 250-char expert posts
    simple_interval_poster.py - Posts at regular intervals
    seo_amplifier.py - Expands posts for Medium/Dev.to
    main.py - Posts from content_queue.json
    generate_content.py - Content generation wrapper

🔑 Required API Keys

Add to GitHub Secrets (for Codespaces) or .env (for local):
Social Platforms

    TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
    LINKEDIN_ACCESS_TOKEN, LINKEDIN_USER_ID
    FACEBOOK_PAGE_ID, FACEBOOK_ACCESS_TOKEN (optional)

AI Generation

    GROQ_API_KEY

SEO Platforms (optional)

    DEVTO_API_KEY
    MEDIUM_ACCESS_TOKEN, MEDIUM_USER_ID

📊 Usage Examples
Generate and Post Expert Content


# Generate 6 expert posts + 1 thread
python expert_content_generator.py

# Post every 30 minutes
python simple_interval_poster.py 30

Generate Blog Content

# Generate from topics
python generate_content.py

# Post to all platforms
python main.py

Check Status

# View expert queue
cat expert_queue.json | python -m json.tool | head -20

# View content queue
cat content_queue.json | python -m json.tool

⚙️ Configuration
Posting Frequency

Edit simple_interval_poster.py:

    Default: 30 minutes
    Pass custom interval: python simple_interval_poster.py 15

Content Topics

Edit in expert_content_generator.py:

    self.topics - AI/ML topics
    self.content_types - Post formats

Platform Selection

Configure in social_poster.py _setup_platforms() method
🚀 Running in Background
Using nohup:

nohup python simple_interval_poster.py > posting.log 2>&1 &

Using screen:
screen -S poster
python simple_interval_poster.py

# Ctrl+A then D to detach

🛠️ Troubleshooting

    ModuleNotFoundError: Install requirements: pip install -r requirements.txt
    API Errors: Check credentials in GitHub Secrets
    Duplicate Posts: Twitter doesn't allow identical posts - content varies automatically

📈 Coming Soon

Medium & Dev.to integration
Analytics dashboard
Web interface

    More platform support

Created by Dr. Carlos Ruiz Viquez 