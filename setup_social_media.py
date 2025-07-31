



#!/usr/bin/env python3
"""
Setup script for social media integration
This script helps users configure their social media API credentials
"""

import os
import json
from pathlib import Path

def create_env_template():
    """Create a .env template file"""
    env_content = """# Social Media API Configuration
# Copy this file to .env and fill in your actual credentials

# Twitter/X API
# Get from: https://developer.twitter.com/en/portal/dashboard
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here

# Reddit API
# Get from: https://www.reddit.com/prefs/apps/
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USERNAME=your_reddit_username_here
REDDIT_PASSWORD=your_reddit_password_here

# LinkedIn API
# Get from: https://www.linkedin.com/developers/apps
LINKEDIN_USERNAME=your_linkedin_email_here
LINKEDIN_PASSWORD=your_linkedin_password_here

# Facebook/Instagram API
# Get from: https://developers.facebook.com/apps/
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token_here
FACEBOOK_APP_ID=your_facebook_app_id_here
FACEBOOK_APP_SECRET=your_facebook_app_secret_here
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token_here

# TikTok API
# Get from: https://developers.tiktok.com/
TIKTOK_ACCESS_TOKEN=your_tiktok_access_token_here
TIKTOK_APP_ID=your_tiktok_app_id_here
TIKTOK_APP_SECRET=your_tiktok_app_secret_here
"""
    
    with open('.env.example', 'w') as f:
        f.write(env_content)
    print("✅ Created .env.example file")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import tweepy
        import praw
        import facebook
        print("✅ All social media dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r plugins/social_mcp/requirements.txt")
        return False

def test_mcp_servers():
    """Test if MCP servers can start"""
    import subprocess
    import time
    
    servers = [
        ("Twitter", 8001, "plugins/social_mcp/twitter_mcp.py"),
        ("Reddit", 8002, "plugins/social_mcp/reddit_mcp.py"),
        ("LinkedIn", 8003, "plugins/social_mcp/linkedin_mcp.py"),
        ("Facebook", 8004, "plugins/social_mcp/facebook_mcp.py"),
        ("TikTok", 8005, "plugins/social_mcp/tiktok_mcp.py"),
    ]
    
    print("\nTesting MCP servers...")
    for name, port, script in servers:
        try:
            process = subprocess.Popen(["python", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(2)
            
            import requests
            response = requests.get(f"http://localhost:{port}/health", timeout=3)
            if response.status_code == 200:
                print(f"✅ {name} MCP server is working")
            else:
                print(f"⚠️  {name} MCP server responded with {response.status_code}")
            
            process.terminate()
            process.wait()
            
        except Exception as e:
            print(f"⚠️  {name} MCP server test failed: {e}")

def main():
    """Main setup function"""
    print("🔧 KaiHands Social Media Integration Setup")
    print("=" * 50)
    
    # Create environment template
    create_env_template()
    
    # Check dependencies
    check_dependencies()
    
    # Test MCP servers
    test_mcp_servers()
    
    print("\n" + "=" * 50)
    print("Setup Complete!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env")
    print("2. Fill in your actual API credentials")
    print("3. Install dependencies: pip install -r plugins/social_mcp/requirements.txt")
    print("4. Start MCP servers: python plugins/social_mcp/test_servers.py")
    print("5. Open KaiHands frontend and go to Social Media tab")
    print("\nFor detailed instructions, see SOCIAL_MEDIA_INTEGRATION.md")

if __name__ == "__main__":
    main()



