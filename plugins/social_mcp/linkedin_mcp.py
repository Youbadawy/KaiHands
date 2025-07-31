



#!/usr/bin/env python3
"""
LinkedIn MCP Server for OpenHands
Provides social media management capabilities for LinkedIn
"""

import os
import asyncio
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from linkedin_api import Linkedin
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LinkedIn MCP Server", version="1.0.0")

# LinkedIn API credentials
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Initialize LinkedIn client (will be None if credentials are missing)
linkedin = None

if LINKEDIN_USERNAME and LINKEDIN_PASSWORD:
    try:
        linkedin = Linkedin(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)
    except Exception as e:
        print(f"Warning: Failed to initialize LinkedIn client: {e}")
        linkedin = None

class PostUpdateRequest(BaseModel):
    text: str
    visibility: str = "PUBLIC"  # PUBLIC, CONNECTIONS, LOGGED_IN

class SearchPeopleRequest(BaseModel):
    keywords: str
    limit: int = 10

class GetProfileRequest(BaseModel):
    username: Optional[str] = None
    profile_id: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "LinkedIn MCP Server is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "linkedin-mcp"}

@app.post("/api/post-update")
async def post_update(request: PostUpdateRequest):
    """Post an update to LinkedIn"""
    try:
        # Note: This is a simplified implementation
        # In production, you'd need proper OAuth flow and token management
        result = linkedin.post_share(
            comment_text=request.text,
            visibility=request.visibility
        )
        
        return {
            "success": True,
            "update_id": result.get("id", ""),
            "text": request.text
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/search-people")
async def search_people(request: SearchPeopleRequest):
    """Search for people on LinkedIn"""
    try:
        results = linkedin.search_people(
            keywords=request.keywords,
            limit=request.limit
        )
        
        return {
            "people": [
                {
                    "name": person.get("name", ""),
                    "headline": person.get("headline", ""),
                    "profile_url": person.get("profile_url", ""),
                    "location": person.get("location", "")
                }
                for person in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/get-profile")
async def get_profile(request: GetProfileRequest):
    """Get LinkedIn profile information"""
    try:
        if request.username:
            profile = linkedin.get_profile(request.username)
        elif request.profile_id:
            profile = linkedin.get_profile(request.profile_id)
        else:
            profile = linkedin.get_user_profile()
        
        return {
            "profile": {
                "name": profile.get("firstName", "") + " " + profile.get("lastName", ""),
                "headline": profile.get("headline", ""),
                "summary": profile.get("summary", ""),
                "location": profile.get("locationName", ""),
                "industry": profile.get("industryName", ""),
                "connections": profile.get("numConnections", 0)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/mcp-tools")
async def get_mcp_tools():
    """Return available MCP tools for LinkedIn"""
    return {
        "tools": [
            {
                "name": "post_update",
                "description": "Post an update to LinkedIn",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Update text content"},
                        "visibility": {"type": "string", "enum": ["PUBLIC", "CONNECTIONS", "LOGGED_IN"], "description": "Post visibility"}
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "search_people",
                "description": "Search for people on LinkedIn",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {"type": "string", "description": "Search keywords"},
                        "limit": {"type": "integer", "description": "Maximum number of results"}
                    },
                    "required": ["keywords"]
                }
            },
            {
                "name": "get_profile",
                "description": "Get LinkedIn profile information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string", "description": "LinkedIn username"},
                        "profile_id": {"type": "string", "description": "LinkedIn profile ID"}
                    }
                }
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)



