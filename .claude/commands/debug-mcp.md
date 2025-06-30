Debug MCP server issues and validate tool functionality.

Issue description: $ARGUMENTS

Follow these steps:

1. Start the MCP server in debug mode: `uv run python -m server.main`
2. Check server logs for any startup errors or warnings
3. Validate tool registration and schema definitions
4. Test each tool individually if specific issue mentioned
5. Check data storage and file permissions
6. Verify MCP protocol compliance
7. Test integration points with Claude Desktop
8. Provide debugging recommendations and fixes

Common debugging areas:
- Tool schema validation
- Async function handling
- File I/O operations
- Error handling and user feedback