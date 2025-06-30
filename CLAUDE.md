# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Tides DXT** is a Model Context Protocol (MCP) server that implements a productivity workflow management system based on natural tidal patterns. It integrates with Claude Desktop to provide rhythmic, sustainable productivity cycles rather than forced productivity.

## Technology Stack

- **Python 3.11+** with async/await patterns
- **MCP SDK** for Claude Desktop integration  
- **Pydantic** for type-safe data validation
- **File-based JSON storage** for simplicity and portability

## Development Commands

This project uses `uv` for fast Python package management:

```bash
# Install dependencies and sync virtual environment
uv sync

# Install with development dependencies
uv sync --extra dev

# Run tests
uv run python -m pytest

# Run tests with coverage
uv run python -m pytest --cov=server --cov-report=term-missing

# Run single test file
uv run python -m pytest tests/test_tools.py

# Run specific test
uv run python -m pytest tests/test_tools.py::test_create_tide_daily

# Start MCP server (for testing)
uv run python -m server.main

# Run linting
uv run ruff check server tests

# Run type checking
uv run mypy server

# Format code
uv run ruff format server tests

# Add new dependency
uv add package-name

# Add development dependency
uv add --optional dev package-name
```

## Architecture

### Core Components

- **MCP Server** (`server/main.py`): Entry point implementing MCP protocol
- **Tool Registry** (`server/tools/`): Three main tools for tidal workflow management
- **Storage Layer** (`server/storage.py`): File-based JSON persistence
- **Type Definitions** (`server/types.py`): Pydantic models for type safety

### Three Core Tools

1. **`create_tide`**: Creates new tidal workflows with intensity levels (gentle/moderate/strong)
2. **`list_tides`**: Retrieves and filters existing tides by type, status, or date
3. **`flow_tide`**: Updates tide progress and captures insights

### Tidal Philosophy

The system is built around natural tidal metaphors:
- **Flow Intensities**: gentle (low energy), moderate (focused work), strong (deep focus)
- **Tide Types**: daily, weekly, project, seasonal
- **Natural Rhythms**: Emphasizes sustainable productivity over forced productivity

### Data Storage

- **File-based JSON**: Simple, portable, version-controllable
- **Default location**: `~/.config/tides-dxt/tides.json`
- **Configurable path**: Via `TIDES_DATA_PATH` environment variable
- **Atomic writes**: Ensures data consistency

## Code Conventions

### Type Safety
- All data models use Pydantic for validation
- Extensive use of type hints throughout
- Enum types for constrained values (TideType, FlowIntensity, TideStatus)

### Async Patterns
- All tool functions are async
- Proper error handling with try/catch blocks
- MCP protocol compliance for async operations

### Error Handling
- Custom exception types where appropriate
- Graceful degradation for missing files
- Clear error messages for user feedback

### Testing
- Comprehensive test coverage with pytest
- Async test support using pytest-asyncio
- Isolated test environment with temporary data files
- Tests cover happy path, edge cases, and error conditions

## Key Files

- `server/main.py`: MCP server entry point and tool registration
- `server/tools/`: Individual tool implementations (create_tide.py, list_tides.py, flow_tide.py)
- `server/storage.py`: Data persistence layer
- `server/types.py`: Core data models and types
- `tests/`: Comprehensive test suite
- `pyproject.toml`: Modern Python project configuration

## MCP Integration

This server is designed to be registered with Claude Desktop:
- Implements standard MCP protocol for tool discovery
- Provides rich tool descriptions for Claude
- Supports complex workflow management through natural language interaction
- Maintains conversation context through persistent storage

## Custom Slash Commands

This project includes custom slash commands in `.claude/commands/` for common workflows:

- `/project:run-tests [pattern]`: Run tests with optional filtering
- `/project:debug-mcp [issue]`: Debug MCP server issues
- `/project:add-tool [name]`: Add new tool following project conventions
- `/project:analyze-tides [focus]`: Analyze tide data and productivity patterns
- `/project:fix-github-issue [number]`: Fix GitHub issues with full workflow
- `/project:write-github-issue [requirements]`: Create well-formatted GitHub issues from planning sessions

Use these commands to streamline development tasks while maintaining project conventions.

## Unique Aspects

- **Tidal Metaphor**: All functionality is built around the concept of natural tides and flows
- **Sustainable Productivity**: Focus on working with natural energy cycles rather than against them
- **Historical Insights**: Tracks patterns over time to help users understand their productivity rhythms
- **Flexible Timeframes**: Supports multiple scales from daily habits to seasonal projects