#!/usr/bin/env python3
"""
Demo of the FastMCP LangGraph documentation server using FastMCP's client capabilities.
"""

import asyncio
from fastmcp.client import Client, PythonStdioTransport

async def demo_fastmcp_client():
    """Demonstrate the FastMCP client connecting to our server."""
    print("Starting FastMCP demo...")

    try:
        # Create client with stdio transport
        transport = PythonStdioTransport("fastmcp_langgraph_server.py")
        async with Client(transport) as client:
            print("Connected to server!")

            # List available resources
            print("\nListing resources...")
            resources = await client.list_resources()
            print(f"Found {len(resources)} resources:")
            for resource in resources:
                print(f"  Resource: {resource.name}")
                print(f"    URI: {resource.uri}")
                print(f"    Description: {resource.description}")

            # List available tools
            print("\nListing tools...")
            tools = await client.list_tools()
            print(f"Found {len(tools)} tools:")
            for tool in tools:
                print(f"  Tool: {tool.name}")
                print(f"    Description: {tool.description}")

            # Read the documentation resource
            print("\nReading LangGraph documentation...")
            if resources:
                resource_uri = resources[0].uri
                content = await client.read_resource(resource_uri)
                if hasattr(content, 'contents') and content.contents:
                    text = content.contents[0].text
                    print(f"    Content length: {len(text):,} characters")
                    print(f"    Preview: {text[:200]}...")
                elif isinstance(content, str):
                    print(f"    Content length: {len(content):,} characters")
                    print(f"    Preview: {content[:200]}...")

            # Test the search tool
            print("\nTesting search tool...")
            search_result = await client.call_tool(
                "search_langgraph_docs",
                {"query": "chatbot"}
            )
            if hasattr(search_result, 'content') and search_result.content:
                search_text = search_result.content[0].text
                print(f"    Search results (first 300 chars): {search_text[:300]}...")
            elif isinstance(search_result, str):
                print(f"    Search results (first 300 chars): {search_result[:300]}...")

            # Test the stats tool
            print("\nGetting documentation statistics...")
            stats_result = await client.call_tool("get_documentation_stats")
            if hasattr(stats_result, 'content') and stats_result.content:
                stats_text = stats_result.content[0].text
                print(f"    Stats:\n{stats_text}")
            elif isinstance(stats_result, str):
                print(f"    Stats:\n{stats_result}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(demo_fastmcp_client())