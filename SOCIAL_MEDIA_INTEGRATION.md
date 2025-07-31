


# Social Media Integration Guide

This guide explains how to set up and use the social media integration features in KaiHands.

## Overview

KaiHands now includes comprehensive social media integration with support for:
- **Twitter/X** - Post tweets, search, user management
- **Reddit** - Submit posts, search subreddits, user info
- **LinkedIn** - Post updates, search people, profile management
- **Facebook/Instagram** - Post to pages, Instagram content, insights
- **TikTok** - Video uploads, analytics, user management

## Architecture

The integration uses a modular MCP (Model Context Protocol) server architecture:
- Each platform has its own MCP server running on a dedicated port
- OAuth 2.0 authentication for secure credential management
- RESTful API endpoints for agent interaction
- Environment-based configuration for security

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the root directory with your API credentials:

```bash
# Twitter/X API
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# Reddit API
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password

# LinkedIn API
LINKEDIN_USERNAME=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password

# Facebook/Instagram API
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token

# TikTok API
TIKTOK_ACCESS_TOKEN=your_tiktok_access_token
TIKTOK_APP_ID=your_tiktok_app_id
TIKTOK_APP_SECRET=your_tiktok_app_secret
```

### 2. Install Dependencies

```bash
cd /workspace/KaiHands/plugins/social_mcp
pip install -r requirements.txt
```

### 3. MCP Server Configuration

Add the social media MCP configurations to your main `config.toml`:

```toml
[mcp_servers.twitter]
name = "Twitter/X MCP Server"
command = "python"
args = ["plugins/social_mcp/twitter_mcp.py"]
port = 8001
enabled = true

[mcp_servers.reddit]
name = "Reddit MCP Server"
command = "python"
args = ["plugins/social_mcp/reddit_mcp.py"]
port = 8002
enabled = true

[mcp_servers.linkedin]
name = "LinkedIn MCP Server"
command = "python"
args = ["plugins/social_mcp/linkedin_mcp.py"]
port = 8003
enabled = true

[mcp_servers.facebook]
name = "Facebook/Instagram MCP Server"
command = "python"
args = ["plugins/social_mcp/facebook_mcp.py"]
port = 8004
enabled = true

[mcp_servers.tiktok]
name = "TikTok MCP Server"
command = "python"
args = ["plugins/social_mcp/tiktok_mcp.py"]
port = 8005
enabled = true
```

### 4. Start MCP Servers

You can start individual servers or all at once:

```bash
# Start all servers
cd /workspace/KaiHands/plugins/social_mcp
python twitter_mcp.py &
python reddit_mcp.py &
python linkedin_mcp.py &
python facebook_mcp.py &
python tiktok_mcp.py &

# Or use the test script
python test_servers.py
```

### 5. Frontend Usage

1. Navigate to the KaiHands frontend at `http://localhost:3000`
2. Click on the "Social Media" tab
3. Connect your accounts using OAuth
4. Use the available actions:
   - **Generate Content**: Create AI-generated posts
   - **Lead Generation**: Find prospects and extract contacts
   - **Follower Interaction**: Reply to comments and DMs
   - **Growth Analytics**: Analyze trends and suggest content

## API Endpoints

Each MCP server provides the following endpoints:

### Twitter/X MCP (Port 8001)
- `POST /api/post-tweet` - Post a tweet
- `GET /api/search-tweets` - Search tweets
- `GET /api/user-info` - Get user information

### Reddit MCP (Port 8002)
- `POST /api/submit-post` - Submit a post to a subreddit
- `POST /api/search-subreddits` - Search for subreddits
- `GET /api/user-info` - Get user information

### LinkedIn MCP (Port 8003)
- `POST /api/post-update` - Post a LinkedIn update
- `POST /api/search-people` - Search for people
- `GET /api/profile` - Get profile information

### Facebook/Instagram MCP (Port 8004)
- `POST /api/post-to-page` - Post to Facebook page
- `POST /api/post-to-instagram` - Post to Instagram
- `GET /api/page-insights` - Get page insights

### TikTok MCP (Port 8005)
- `POST /api/upload-video` - Upload a TikTok video
- `GET /api/user-info` - Get user information
- `GET /api/video-analytics` - Get video analytics

## Usage Examples

### Content Generation
```
"Generate a LinkedIn post about AI in healthcare and post it to my profile"
```

### Lead Generation
```
"Find Reddit users interested in machine learning in r/MachineLearning and extract their contact info"
```

### Follower Interaction
```
"Reply to recent Twitter mentions with personalized thank you messages"
```

### Growth Analytics
```
"Analyze trending hashtags on TikTok for the #AI category and suggest content ideas"
```

## Security Notes

- All credentials are stored in environment variables
- OAuth tokens are never hardcoded
- Rate limiting is implemented for all platforms
- Error handling includes graceful degradation
- No passwords are stored in the system

## Troubleshooting

### Common Issues

1. **"Client not configured" error**
   - Check that all required environment variables are set
   - Verify credentials are correct

2. **Rate limiting**
   - All servers implement exponential backoff
   - Check platform-specific rate limits

3. **Authentication failures**
   - Ensure OAuth tokens are valid and not expired
   - Re-authenticate if necessary

### Testing

Run the test script to verify all servers:
```bash
cd /workspace/KaiHands/plugins/social_mcp
python test_servers.py
```

## Development

### Adding New Platforms

To add a new social media platform:

1. Create a new MCP server file in `plugins/social_mcp/`
2. Follow the existing pattern with FastAPI
3. Add environment variables to `.env.example`
4. Update the configuration files
5. Add frontend components as needed

### MCP Server Template

Use this template for new platforms:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Optional, List

app = FastAPI(title="Your Platform MCP", version="1.0.0")

# Environment variables
YOUR_PLATFORM_TOKEN = os.getenv("YOUR_PLATFORM_TOKEN")

# Initialize client
client = None
if YOUR_PLATFORM_TOKEN:
    # Initialize your platform client

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "your-platform-mcp"}

@app.get("/api/mcp-tools")
async def get_mcp_tools():
    return {
        "tools": [
            {
                "name": "your_action",
                "description": "Description of the action",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param1": {"type": "string", "description": "Parameter description"}
                    },
                    "required": ["param1"]
                }
            }
        ]
    }

# Add your endpoints here
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review server logs for specific error messages
3. Ensure all dependencies are installed correctly
4. Verify environment variable configuration


