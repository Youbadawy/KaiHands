




#!/usr/bin/env python3
"""
Test script for social media MCP servers
"""

import subprocess
import time
import requests
import json

def test_server(name, port, script_path):
    """Test a single MCP server"""
    print(f"Testing {name} server...")
    
    # Start the server
    process = subprocess.Popen(
        ["python", script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test health endpoint
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ {name} health check passed")
            
            # Test MCP tools endpoint
            response = requests.get(f"http://localhost:{port}/api/mcp-tools", timeout=5)
            if response.status_code == 200:
                tools = response.json()
                print(f"✅ {name} MCP tools endpoint working ({len(tools.get('tools', []))} tools available)")
                return True
            else:
                print(f"❌ {name} MCP tools endpoint failed: {response.status_code}")
        else:
            print(f"❌ {name} health check failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ {name} server not responding: {e}")
    finally:
        process.terminate()
        process.wait()
    
    return False

def main():
    """Test all MCP servers"""
    servers = [
        ("Twitter", 8001, "twitter_mcp.py"),
        ("Reddit", 8002, "reddit_mcp.py"),
        ("LinkedIn", 8003, "linkedin_mcp.py"),
        ("Facebook/Instagram", 8004, "facebook_mcp.py"),
        ("TikTok", 8005, "tiktok_mcp.py"),
    ]
    
    results = []
    for name, port, script in servers:
        success = test_server(name, port, script)
        results.append((name, success))
    
    print("\n" + "="*50)
    print("Test Results:")
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    print(f"\n{passed}/{len(results)} servers working")
    
    return passed == len(results)

if __name__ == "__main__":
    main()




