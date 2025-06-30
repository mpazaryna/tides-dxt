Analyze and fix the GitHub issue for Tides DXT project.

Issue number or description: $ARGUMENTS

Follow these steps:

1. Use `gh issue view $ARGUMENTS` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files using grep/find
4. Analyze the current implementation and identify the root cause
5. Implement necessary changes following project conventions:
   - Maintain async patterns and type safety
   - Follow tidal metaphor naming
   - Add proper error handling
6. Write and run tests to verify the fix
7. Run full test suite: `uv run python -m pytest --cov=server --cov-report=term-missing`
8. Ensure code passes any linting if configured
9. Create a descriptive commit message following project style
10. Push changes and create a PR using `gh pr create`

Project-specific considerations:
- Maintain MCP protocol compliance
- Preserve tidal philosophy and metaphors
- Update documentation if needed
- Test with actual MCP server integration