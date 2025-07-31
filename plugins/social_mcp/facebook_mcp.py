




#!/usr/bin/env python3
"""
Facebook/Instagram MCP Server for OpenHands
Provides social media management capabilities for Facebook and Instagram
"""

import os
import asyncio
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import facebook
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Facebook/Instagram MCP Server", version="1.0.0")

# Facebook API credentials
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")

# Initialize Facebook Graph API
graph = None

if FACEBOOK_ACCESS_TOKEN:
    try:
        graph = facebook.GraphAPI(access_token=FACEBOOK_ACCESS_TOKEN, version="18.0")
    except Exception as e:
        print(f"Warning: Failed to initialize Facebook client: {e}")
        graph = None

class PostToPageRequest(BaseModel):
    page_id: str
    message: str
    link: Optional[str] = None

class PostToInstagramRequest(BaseModel):
    instagram_account_id: str
    image_url: str
    caption: Optional[str] = None

class GetPageInsightsRequest(BaseModel):
    page_id: str
    metric: str
    period: str = "day"

@app.get("/")
async def root():
    return {"message": "Facebook/Instagram MCP Server is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "facebook-instagram-mcp"}

@app.post("/api/post-to-page")
async def post_to_page(request: PostToPageRequest):
    """Post to Facebook page"""
    try:
        result = graph.put_object(
            parent_object=request.page_id,
            connection_name="feed",
            message=request.message,
            link=request.link
        )
        
        return {
            "success": True,
            "post_id": result["id"],
            "message": request.message
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/post-to-instagram")
async def post_to_instagram(request: PostToInstagramRequest):
    """Post to Instagram account"""
    try:
        # Create media object
        media_creation = graph.put_object(
            parent_object=request.instagram_account_id,
            connection_name="media",
            image_url=request.image_url,
            caption=request.caption
        )
        
        # Publish the media
        publish_result = graph.put_object(
            parent_object=request.instagram_account_id,
            connection_name="media_publish",
            creation_id=media_creation["id"]
        )
        
        return {
            "success": True,
            "media_id": publish_result["id"],
            "caption": request.caption
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/get-page-insights")
async def get_page_insights(request: GetPageInsightsRequest):
    """Get Facebook page insights"""
    try:
        insights = graph.get_object(
            f"{request.page_id}/insights",
            metric=request.metric,
            period=request.period
        )
        
        return {
            "insights": insights.get("data", [])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/get-pages")
async def get_pages():
    """Get Facebook pages managed by the user"""
    try:
        pages = graph.get_object("me/accounts")
        
        return {
            "pages": [
                {
                    "id": page["id"],
                    "name": page["name"],
                    "category": page.get("category", ""),
                    "access_token": page.get("access_token", "")
                }
                for page in pages.get("data", [])
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/get-instagram-accounts")
async def get_instagram_accounts():
    """Get Instagram accounts linked to Facebook pages"""
    try:
        accounts = graph.get_object("me/accounts", fields="instagram_business_account{id,name,username}")
        
        instagram_accounts = []
        for page in accounts.get("data", []):
            ig_account = page.get("instagram_business_account")
            if ig_account:
                instagram_accounts.append({
                    "id": ig_account["id"],
                    "name": ig_account["name"],
                    "username": ig_account["username"]
                })
        
        return {"instagram_accounts": instagram_accounts}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/mcp-tools")
async def get_mcp_tools():
    """Return available MCP tools for Facebook/Instagram"""
    return {
        "tools": [
            {
                "name": "post_to_page",
                "description": "Post to Facebook page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "Facebook page ID"},
                        "message": {"type": "string", "description": "Post message"},
                        "link": {"type": "string", "description": "Optional link URL"}
                    },
                    "required": ["page_id", "message"]
                }
            },
            {
                "name": "post_to_instagram",
                "description": "Post to Instagram account",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instagram_account_id": {"type": "string", "description": "Instagram account ID"},
                        "image_url": {"type": "string", "description": "Image URL to post"},
                        "caption": {"type": "string", "description": "Post caption"}
                    },
                    "required": ["instagram_account_id", "image_url"]
                }
            },
            {
                "name": "get_page_insights",
                "description": "Get Facebook page insights",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "Facebook page ID"},
                        "metric": {"type": "string", "description": "Metric to retrieve"},
                        "period": {"type": "string", "enum": ["day", "week", "days_28"], "description": "Time period"}
                    },
                    "required": ["page_id", "metric"]
                }
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)




