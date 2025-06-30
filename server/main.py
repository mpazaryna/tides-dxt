#!/usr/bin/env python3
"""
Tides MCP Server

A rhythmic workflow management system inspired by natural tidal patterns.
Helps create sustainable productivity cycles through tidal flows.
"""

import asyncio
import logging
import sys

import mcp.server.stdio
from mcp import types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from tools.tide_tools import tide_handlers, tide_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)

logger = logging.getLogger(__name__)


# Create the MCP server instance
server = Server("tides")


# Register tool handlers
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return tide_tools


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Call a tool by name"""
    if name not in tide_handlers:
        raise ValueError(f"Unknown tool: {name}")

    result = await tide_handlers[name](arguments)

    return [types.TextContent(type="text", text=str(result))]


async def main():
    """Main server function"""
    logger.info("🌊 Starting Tides MCP Server...")

    # Server options
    options = InitializationOptions(
        server_name="tides",
        server_version="0.1.0",
        capabilities=server.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={},
        ),
    )

    # Run the server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            options,
        )


if __name__ == "__main__":
    asyncio.run(main())
