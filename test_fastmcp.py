#!/usr/bin/env python3
"""
Test client for the FastMCP LangGraph documentation server.
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, Optional

class FastMCPClient:
    """Simple client to test the FastMCP LangGraph documentation server."""

    def __init__(self, server_command: list):
        self.server_command = server_command
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0

    async def start_server(self):
        """Start the FastMCP server process."""
        self.process = subprocess.Popen(
            self.server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )

    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a JSON-RPC request to the server."""
        if not self.process:
            raise RuntimeError("Server not started")

        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method
        }

        if params:
            request["params"] = params

        # Send request
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json)
        self.process.stdin.flush()

        # Read response
        response_line = self.process.stdout.readline()
        if not response_line:
            raise RuntimeError("No response from server")

        return json.loads(response_line.strip())

    async def initialize(self):
        """Initialize the MCP connection."""
        response = await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "resources": {"subscribe": False},
                "tools": {}
            },
            "clientInfo": {
                "name": "fastmcp-test-client",
                "version": "1.0.0"
            }
        })
        return response

    async def list_resources(self):
        """List available resources."""
        response = await self.send_request("resources/list")
        return response

    async def read_resource(self, uri: str):
        """Read a specific resource."""
        response = await self.send_request("resources/read", {"uri": uri})
        return response

    async def list_tools(self):
        """List available tools."""
        response = await self.send_request("tools/list")
        return response

    async def call_tool(self, name: str, arguments: Dict[str, Any] = None):
        """Call a specific tool."""
        response = await self.send_request("tools/call", {
            "name": name,
            "arguments": arguments or {}
        })
        return response

    def stop_server(self):
        """Stop the FastMCP server process."""
        if self.process:
            self.process.terminate()
            self.process.wait()

async def main():
    """Main test function."""
    # Create client
    client = FastMCPClient(["python", "fastmcp_langgraph_server.py"])

    try:
        print("Starting FastMCP server...")
        await client.start_server()

        print("Initializing connection...")
        init_response = await client.initialize()
        print(f"Server initialized: {init_response['result']['serverInfo']['name']}")

        print("\nListing resources...")
        list_response = await client.list_resources()
        resources = list_response.get("result", {}).get("resources", [])
        for resource in resources:
            print(f"   Resource: {resource['name']}: {resource['uri']}")

        print("\nListing tools...")
        tools_response = await client.list_tools()
        tools = tools_response.get("result", {}).get("tools", [])
        for tool in tools:
            print(f"   Tool: {tool['name']}: {tool['description']}")

        print("\nReading LangGraph documentation resource...")
        read_response = await client.read_resource("file://langgraph-docs")
        if "result" in read_response and "contents" in read_response["result"]:
            content = read_response["result"]["contents"][0]["text"]
            print(f"   Content preview (first 300 chars):\n   {content[:300]}...")
            print(f"   Total content length: {len(content):,} characters")
        else:
            print(f"   Error reading resource: {read_response}")

        print("\nGetting documentation statistics...")
        stats_response = await client.call_tool("get_documentation_stats")
        if "result" in stats_response and "content" in stats_response["result"]:
            stats = stats_response["result"]["content"][0]["text"]
            print(f"   {stats}")

        print("\nSearching for 'chatbot' in documentation...")
        search_response = await client.call_tool("search_langgraph_docs", {"query": "chatbot"})
        if "result" in search_response and "content" in search_response["result"]:
            search_results = search_response["result"]["content"][0]["text"]
            # Show first 500 characters of search results
            print(f"   Search results preview:\n   {search_results[:500]}...")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("\nStopping server...")
        client.stop_server()

if __name__ == "__main__":
    asyncio.run(main())