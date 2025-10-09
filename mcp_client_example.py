#!/usr/bin/env python3
"""
Example MCP client to interact with the LangGraph documentation server.
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, Optional

class MCPClient:
    """Simple MCP client for testing the LangGraph documentation server."""

    def __init__(self, server_command: list):
        self.server_command = server_command
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0

    async def start_server(self):
        """Start the MCP server process."""
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
                "resources": {
                    "subscribe": False
                }
            },
            "clientInfo": {
                "name": "langgraph-docs-client",
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

    def stop_server(self):
        """Stop the MCP server process."""
        if self.process:
            self.process.terminate()
            self.process.wait()

async def main():
    """Main example function."""
    # Create client
    client = MCPClient(["python", "mcp_langgraph_server.py"])

    try:
        print("Starting MCP server...")
        await client.start_server()

        print("Initializing connection...")
        init_response = await client.initialize()
        print(f"Initialize response: {json.dumps(init_response, indent=2)}")

        print("\nListing resources...")
        list_response = await client.list_resources()
        print(f"Resources: {json.dumps(list_response, indent=2)}")

        print("\nReading LangGraph documentation resource...")
        read_response = await client.read_resource("file://langgraph_docs")

        if "result" in read_response and "contents" in read_response["result"]:
            content = read_response["result"]["contents"][0]["text"]
            # Show first 500 characters
            print(f"Content preview (first 500 chars):\n{content[:500]}...")
            print(f"\nTotal content length: {len(content)} characters")
        else:
            print(f"Error reading resource: {read_response}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("\nStopping server...")
        client.stop_server()

if __name__ == "__main__":
    asyncio.run(main())