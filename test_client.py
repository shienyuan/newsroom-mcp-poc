#!/usr/bin/env python3
"""Test client for Newsroom MCP server with OAuth authentication."""

import asyncio
import sys
from fastmcp import Client


async def test_server():
    """Test the MCP server with OAuth authentication."""
    print("=" * 60)
    print("Testing Newsroom MCP Server")
    print("=" * 60)
    print()

    server_url = "http://localhost:8000/mcp"

    print(f"Connecting to: {server_url}")
    print("Note: This will open your browser for Azure OAuth authentication")
    print("      (unless you have a cached token from a previous session)")
    print()
    print("💡 Tip: Run with --clear-cache to force fresh authentication")
    print("   Example: python test_client.py --clear-cache")
    print()
    
    try:
        async with Client(server_url, auth="oauth") as client:
            print("✅ Successfully authenticated!")
            print()
            
            # Test 1: List available resources
            print("📦 Testing Resources...")
            resources = await client.list_resources()
            print(f"   Found {len(resources)} resource(s):")
            for resource in resources:
                print(f"   - {resource.name}: {resource.description}")
            print()
            
            # Test 2: Read the sample_data resource
            print("📖 Reading sample_data resource...")
            sample_data = await client.read_resource("sample://data")
            print(f"   Data: {sample_data}")
            print()
            
            # Test 3: List available tools
            print("🔧 Testing Tools...")
            tools = await client.list_tools()
            print(f"   Found {len(tools)} tool(s):")
            for tool in tools:
                print(f"   - {tool.name}: {tool.description}")
            print()
            
            # Test 4: Call the echo tool
            print("🔊 Calling echo tool...")
            echo_result = await client.call_tool("echo", {"message": "Hello from test client!"})
            print(f"   Echo response: {echo_result.data}")
            print()

            # Test 5: Call the server_info tool
            print("ℹ️  Calling server_info tool...")
            info_result = await client.call_tool("server_info", {})
            # The result is in the structured_content attribute
            info_data = info_result.structured_content
            print(f"   Server: {info_data.get('name')} v{info_data.get('version')}")
            print(f"   Auth: {info_data.get('authentication')}")
            print(f"   Features: {info_data.get('features')}")
            print()
            
            # Test 6: List available prompts
            print("💬 Testing Prompts...")
            prompts = await client.list_prompts()
            print(f"   Found {len(prompts)} prompt(s):")
            for prompt in prompts:
                print(f"   - {prompt.name}: {prompt.description}")
            print()
            
            # Test 7: Get the greeting_template prompt
            print("👋 Getting greeting_template prompt...")
            greeting = await client.get_prompt("greeting_template", {
                "name": "Alice",
                "style": "formal"
            })
            print(f"   Prompt messages: {len(greeting.messages)}")
            for msg in greeting.messages:
                print(f"   - {msg.role}: {msg.content}")
            print()
            
            print("=" * 60)
            print("✅ All tests passed!")
            print("=" * 60)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    # Check if user wants to clear OAuth cache
    if len(sys.argv) > 1 and sys.argv[1] == "--clear-cache":
        import os
        import shutil
        cache_dir = os.path.expanduser("~/.fastmcp/oauth-mcp-client-cache")
        if os.path.exists(cache_dir):
            print(f"🗑️  Clearing OAuth cache: {cache_dir}")
            shutil.rmtree(cache_dir)
            print("✅ Cache cleared! You will be prompted to authenticate again.")
            print()

    success = asyncio.run(test_server())
    exit(0 if success else 1)

