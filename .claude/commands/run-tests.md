Run comprehensive tests for the Tides DXT project with optional filtering.

Test target: $ARGUMENTS

Follow these steps:

1. If $ARGUMENTS is provided, run specific tests matching that pattern
2. If no arguments, run full test suite with coverage
3. Display test results and coverage report
4. If any tests fail, analyze the failures and suggest fixes
5. Ensure all tests pass before completing

Commands to use:
- Full test suite: `uv run python -m pytest --cov=server --cov-report=term-missing`
- Specific test file: `uv run python -m pytest tests/test_$ARGUMENTS.py`
- Specific test function: `uv run python -m pytest -k "$ARGUMENTS"`