#!/usr/bin/env python3
"""
FastMCP Server for LangGraph Documentation
Serves the langgraph_llms.txt file as an MCP resource using the FastMCP framework.
"""

from pathlib import Path
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("LangGraph Documentation Server")

# Path to the LangGraph documentation file
DOCS_FILE = Path(__file__).parent / "langgraph_llms.txt"

@mcp.resource("file://langgraph-docs")
def get_langgraph_docs() -> str:
    """
    Provides comprehensive LangGraph documentation including guides, tutorials,
    concepts, examples, and troubleshooting information.

    This resource contains a complete index of LangGraph documentation covering:
    - Guides: Basic setup, building chatbots, adding tools and memory
    - Agent Development: Prebuilt components, running agents, streaming
    - Advanced Features: Multi-agent systems, human-in-the-loop, time travel
    - Platform: Deployment options, authentication, scaling
    - Examples: Practical implementations and use cases
    - Troubleshooting: Common errors and solutions
    """
    try:
        with open(DOCS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: Documentation file {DOCS_FILE} not found"
    except Exception as e:
        return f"Error reading documentation: {str(e)}"

@mcp.tool()
def search_langgraph_docs(query: str) -> str:
    """
    Search through the LangGraph documentation for specific topics.

    Args:
        query: The search term or topic to look for in the documentation

    Returns:
        Relevant sections from the documentation that match the query
    """
    try:
        with open(DOCS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple case-insensitive search
        lines = content.split('\n')
        matching_lines = []

        for i, line in enumerate(lines):
            if query.lower() in line.lower():
                # Include context (previous and next lines)
                start = max(0, i - 1)
                end = min(len(lines), i + 2)
                context = lines[start:end]
                matching_lines.extend(context)
                matching_lines.append("---")

        if matching_lines:
            result = '\n'.join(matching_lines)
            return f"Found {len([l for l in matching_lines if query.lower() in l.lower()])} matches for '{query}':\n\n{result}"
        else:
            return f"No matches found for '{query}' in the LangGraph documentation."

    except FileNotFoundError:
        return f"Error: Documentation file {DOCS_FILE} not found"
    except Exception as e:
        return f"Error searching documentation: {str(e)}"

@mcp.tool()
def get_documentation_stats() -> str:
    """
    Get statistics about the LangGraph documentation.

    Returns:
        Basic statistics about the documentation content
    """
    try:
        with open(DOCS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        words = content.split()

        # Count different types of entries
        guides_count = content.count('https://langchain-ai.github.io/langgraph/')
        tutorial_count = content.lower().count('tutorial')
        example_count = content.lower().count('example')

        stats = f"""LangGraph Documentation Statistics:

Total Characters: {len(content):,}
Total Lines: {len(lines):,}
Total Words: {len(words):,}
Total Links: {guides_count}
Tutorial References: {tutorial_count}
Example References: {example_count}

File Path: {DOCS_FILE}
File Size: {DOCS_FILE.stat().st_size if DOCS_FILE.exists() else 'N/A'} bytes
"""
        return stats

    except FileNotFoundError:
        return f"Error: Documentation file {DOCS_FILE} not found"
    except Exception as e:
        return f"Error getting documentation stats: {str(e)}"

if __name__ == "__main__":
    # Run the FastMCP server with stdio transport for VS Code
    mcp.run(transport='stdio')