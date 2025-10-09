# LangGraph Documentation FastMCP Server

A Model Context Protocol (MCP) server built with FastMCP that serves the comprehensive LangGraph documentation from `langgraph_llms.txt` as resources and tools for AI assistants and other MCP clients.

## Features

- **📄 Resource Access**: Provides the complete LangGraph documentation as an MCP resource
- **🔍 Search Tool**: Search through the documentation for specific topics
- **📊 Statistics Tool**: Get detailed statistics about the documentation content
- **⚡ FastMCP Framework**: Built using the modern FastMCP framework for high performance
- **🔌 Standard MCP Protocol**: Compatible with any MCP client including Claude Code

## Files

- `fastmcp_langgraph_server.py` - The main FastMCP server implementation
- `fastmcp_config.json` - Configuration file for MCP clients
- `fastmcp_demo.py` - Demonstration client showing all features
- `langgraph_llms.txt` - The comprehensive LangGraph documentation resource

## Installation

Make sure you have FastMCP installed:

```bash
uv add fastmcp
```

Or with pip:

```bash
pip install fastmcp
```

## Usage

### Running the Server

```bash
python fastmcp_langgraph_server.py
or 
uv run fastmcp_langgraph_server.py
```

The server will start and display connection information.

### Testing with Demo Client

```bash
python fastmcp_demo.py
or 
uv run fastmcp_demo.py
```

This demonstrates all server capabilities:
- Lists available resources and tools
- Reads the documentation content
- Searches for specific terms
- Shows documentation statistics

### Configuration for MCP Clients

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "langgraph-fastmcp": {
      "command": "python",
      "args": ["fastmcp_langgraph_server.py"],
      "cwd": "C:\\Users\\user\\Sematic_Search_Implementation_RAG"
    }
  }
}
```

## Available Resources

### `file://langgraph-docs/`
**LangGraph Documentation Resource**
- Complete index of LangGraph documentation
- 69,578 characters of content
- 140 documentation links
- Covers guides, tutorials, concepts, examples, and troubleshooting

## Available Tools

### `search_langgraph_docs`
Search through the LangGraph documentation for specific topics.

**Parameters:**
- `query` (string): The search term or topic to look for

**Returns:**
- Matching sections with context from the documentation

### `get_documentation_stats`
Get comprehensive statistics about the LangGraph documentation.

**Returns:**
- Character count, line count, word count
- Number of links and references
- File information

## Documentation Content

The `langgraph_llms.txt` file contains a comprehensive index of LangGraph documentation including:

### 📚 Guides
- Basic setup and quickstart
- Building chatbots with memory
- Adding tools and web search integration
- Human-in-the-loop controls
- State customization and time travel

### 🤖 Agent Development
- Prebuilt components and architectures
- Running and streaming agents
- Tool integration and customization
- Context and memory management

### 🚀 Advanced Features
- Multi-agent systems and supervisor patterns
- Human-in-the-loop workflows
- Time travel and debugging capabilities
- Subgraphs and complex architectures

### ☁️ Platform & Deployment
- LangGraph Platform overview
- Cloud SaaS and self-hosted options
- Authentication and access control
- Scaling and resilience features

### 💡 Examples & Tutorials
- Agentic RAG systems
- SQL agents and database integration
- Multi-agent supervisor systems
- Authentication and authorization setups

### 🔧 Troubleshooting
- Common error resolution
- Performance optimization
- Debugging tools and techniques

## Example Usage

```python
from fastmcp.client import Client, PythonStdioTransport

async with Client(PythonStdioTransport("fastmcp_langgraph_server.py")) as client:
    # List resources
    resources = await client.list_resources()

    # Search documentation
    results = await client.call_tool("search_langgraph_docs", {"query": "chatbot"})

    # Get statistics
    stats = await client.call_tool("get_documentation_stats")
```

## Benefits for AI Assistants

This MCP server enables AI assistants to:
- Access comprehensive, up-to-date LangGraph documentation
- Search for specific topics and examples
- Provide accurate guidance on LangGraph development
- Reference specific documentation links and tutorials
- Help with troubleshooting and best practices

## Server Statistics

- **Total Documentation**: 69,578 characters
- **Documentation Links**: 140 unique resources
- **Tutorial References**: 32 tutorials
- **Example References**: 59 practical examples
- **Coverage**: Complete LangGraph ecosystem documentation

The server provides fast, searchable access to this wealth of information for any MCP-compatible AI assistant or development tool.