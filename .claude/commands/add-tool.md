Add a new tool to the Tides DXT MCP server following project conventions.

Tool name and description: $ARGUMENTS

Follow these steps:

1. Create new tool file in `server/tools/` directory
2. Implement tool function following async patterns and type safety
3. Add Pydantic schema for tool parameters
4. Register tool in `server/main.py`
5. Add comprehensive tests in `tests/` directory
6. Update type definitions in `server/types.py` if needed
7. Test tool functionality with MCP server
8. Run full test suite to ensure no regressions: `uv run python -m pytest --cov=server --cov-report=term-missing`
9. Update CLAUDE.md documentation if significant addition

Tool conventions:
- Use async/await patterns
- Implement proper error handling
- Follow tidal metaphor naming
- Include detailed docstrings
- Add parameter validation with Pydantic