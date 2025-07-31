



#!/usr/bin/env python3
"""
Reddit MCP Server for OpenHands
Provides social media management capabilities for Reddit
"""

import os
import asyncio
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import praw
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Reddit MCP Server", version="1.0.0")

# Reddit API credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "OpenHands/1.0")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

# Initialize Reddit client
reddit = None

if all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD]):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD
    )

class SubmitPostRequest(BaseModel):
    subreddit: str
    title: str
    text: Optional[str] = None
    url: Optional[str] = None
    kind: str = "self"  # self, link, image, video

class SearchSubredditsRequest(BaseModel):
    query: str
    limit: int = 10

class GetUserRequest(BaseModel):
    username: str

@app.get("/")
async def root():
    return {"message": "Reddit MCP Server is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "reddit-mcp"}

@app.post("/api/submit-post")
async def submit_post(request: SubmitPostRequest):
    """Submit a post to Reddit"""
    try:
        subreddit = reddit.subreddit(request.subreddit)
        
        if request.kind == "self":
            submission = subreddit.submit(request.title, selftext=request.text or "")
        elif request.kind == "link":
            submission = subreddit.submit(request.title, url=request.url)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported post kind: {request.kind}")
        
        return {
            "success": True,
            "post_id": submission.id,
            "post_url": submission.url,
            "title": submission.title
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/search-subreddits")
async def search_subreddits(request: SearchSubredditsRequest):
    """Search for subreddits"""
    try:
        subreddits = reddit.subreddits.search(request.query, limit=request.limit)
        
        return {
            "subreddits": [
                {
                    "name": subreddit.display_name,
                    "title": subreddit.title,
                    "description": subreddit.public_description,
                    "subscribers": subreddit.subscribers,
                    "url": f"https://reddit.com{subreddit.url}"
                }
                for subreddit in subreddits
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/get-user")
async def get_user(request: GetUserRequest):
    """Get Reddit user information"""
    try:
        user = reddit.redditor(request.username)
        
        # Load user data
        user_data = {
            "name": user.name,
            "karma": user.link_karma + user.comment_karma,
            "created_utc": user.created_utc,
            "is_verified": user.has_verified_email if hasattr(user, 'has_verified_email') else None
        }
        
        return user_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/get-me")
async def get_me():
    """Get authenticated user information"""
    try:
        user = reddit.user.me()
        
        return {
            "name": user.name,
            "karma": user.link_karma + user.comment_karma,
            "created_utc": user.created_utc,
            "is_verified": user.has_verified_email if hasattr(user, 'has_verified_email') else None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/search-posts")
async def search_posts(request: SearchSubredditsRequest):
    """Search for posts across Reddit"""
    try:
        posts = reddit.subreddit("all").search(request.query, limit=request.limit)
        
        return {
            "posts": [
                {
                    "id": post.id,
                    "title": post.title,
                    "url": post.url,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "subreddit": post.subreddit.display_name,
                    "author": post.author.name if post.author else "[deleted]"
                }
                for post in posts
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/mcp-tools")
async def get_mcp_tools():
    """Return available MCP tools for Reddit"""
    return {
        "tools": [
            {
                "name": "submit_post",
                "description": "Submit a post to Reddit",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subreddit": {"type": "string", "description": "Subreddit name"},
                        "title": {"type": "string", "description": "Post title"},
                        "text": {"type": "string", "description": "Post text content"},
                        "url": {"type": "string", "description": "URL for link posts"},
                        "kind": {"type": "string", "enum": ["self", "link"], "description": "Type of post"}
                    },
                    "required": ["subreddit", "title"]
                }
            },
            {
                "name": "search_subreddits",
                "description": "Search for subreddits",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "limit": {"type": "integer", "description": "Maximum number of results"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "search_posts",
                "description": "Search for posts across Reddit",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "limit": {"type": "integer", "description": "Maximum number of results"}
                    },
                    "required": ["query"]
                }
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)



