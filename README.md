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

```bash
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
