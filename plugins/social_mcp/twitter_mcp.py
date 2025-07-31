


#!/usr/bin/env python3
"""
Twitter/X MCP Server for OpenHands
Provides social media management capabilities for Twitter/X
"""

import os
import json
import asyncio
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import tweepy
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Twitter/X MCP Server", version="1.0.0")

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Initialize Twitter client (will be None if credentials are missing)
api = None
client = None

if TWITTER_API_KEY and TWITTER_API_SECRET and TWITTER_ACCESS_TOKEN and TWITTER_ACCESS_TOKEN_SECRET:
    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY,
        TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)

if TWITTER_BEARER_TOKEN:
    client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

class PostTweetRequest(BaseModel):
    text: str
    media_ids: Optional[List[str]] = None

class SearchTweetsRequest(BaseModel):
    query: str
    max_results: int = 10
    tweet_fields: List[str] = ["created_at", "author_id", "public_metrics"]

class GetUserRequest(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Twitter/X MCP Server is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "twitter-mcp"}

@app.post("/api/post-tweet")
async def post_tweet(request: PostTweetRequest):
    """Post a tweet to Twitter/X"""
    if not client:
        raise HTTPException(
            status_code=503, 
            detail="Twitter client not configured. Please set TWITTER_BEARER_TOKEN environment variable."
        )
    
    try:
        response = client.create_tweet(text=request.text)
        return {
            "success": True,
            "tweet_id": response.data["id"],
            "text": request.text
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/search-tweets")
async def search_tweets(request: SearchTweetsRequest):
    """Search for tweets"""
    if not client:
        raise HTTPException(
            status_code=503, 
            detail="Twitter client not configured. Please set TWITTER_BEARER_TOKEN environment variable."
        )
    
    try:
        tweets = client.search_recent_tweets(
            query=request.query,
            max_results=request.max_results,
            tweet_fields=request.tweet_fields
        )
        
        return {
            "tweets": [
                {
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": str(tweet.created_at),
                    "author_id": tweet.author_id,
                    "public_metrics": tweet.public_metrics
                }
                for tweet in tweets.data or []
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/get-user")
async def get_user(request: GetUserRequest):
    """Get user information"""
    if not client:
        raise HTTPException(
            status_code=503, 
            detail="Twitter client not configured. Please set TWITTER_BEARER_TOKEN environment variable."
        )
    
    try:
        if request.username:
            user = client.get_user(username=request.username)
        elif request.user_id:
            user = client.get_user(id=request.user_id)
        else:
            raise HTTPException(status_code=400, detail="Either username or user_id must be provided")
        
        return {
            "id": user.data.id,
            "name": user.data.name,
            "username": user.data.username,
            "description": user.data.description,
            "public_metrics": user.data.public_metrics
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/get-me")
async def get_me():
    """Get authenticated user information"""
    try:
        me = client.get_me()
        return {
            "id": me.data.id,
            "name": me.data.name,
            "username": me.data.username,
            "description": me.data.description,
            "public_metrics": me.data.public_metrics
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/mcp-tools")
async def get_mcp_tools():
    """Return available MCP tools for Twitter/X"""
    return {
        "tools": [
            {
                "name": "post_tweet",
                "description": "Post a tweet to Twitter/X",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Tweet text content"},
                        "media_ids": {"type": "array", "items": {"type": "string"}, "description": "Optional media IDs"}
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "search_tweets",
                "description": "Search for tweets",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "max_results": {"type": "integer", "description": "Maximum number of results (1-100)"},
                        "tweet_fields": {"type": "array", "items": {"type": "string"}, "description": "Fields to include in response"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_user",
                "description": "Get user information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string", "description": "Twitter username"},
                        "user_id": {"type": "string", "description": "Twitter user ID"}
                    }
                }
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)


