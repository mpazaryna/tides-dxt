# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.1] - 2025-07-01

### Fixed
- **Import Path Compatibility**: Add try/except block for imports to work in both development and DXT environments
  - Fixes ModuleNotFoundError when running as Claude Desktop extension
  - Maintains compatibility with pytest and local development

## [0.3.0] - 2025-06-30

### Added
- **Automated Release Command**: New `/project:package-release` custom command for streamlined releases
  - Automates version updates, changelog management, and package building
  - Includes pre-release checks for tests, linting, and type safety
  - Creates versioned DXT packages automatically

### Fixed
- **Storage Path Initialization**: Improved default storage handling for better first-run experience
  - Changed default path from `./tides_data` to `~/Documents/tides_data`
  - Added fallback logic when default path isn't writable
  - Better error messages for permission issues
- **Import Paths**: Fixed relative import issues in tide_tools.py for proper test execution

## [0.2.0] - 2025-06-30

### Added
- **End Tide Tool**: New `end_tide` tool allows users to complete or pause tidal workflows before their natural conclusion
  - Support for both "completed" and "paused" status options
  - Optional completion notes to capture insights and learnings
  - Smart validation prevents ending already completed/paused tides
  - Integration with flow history tracking
- **DXT Package Support**: Full implementation of Anthropic's DXT format for Claude Desktop integration
  - Self-contained package with all dependencies included
  - Proper manifest configuration with user settings
  - Automatic dependency resolution and packaging
- **Comprehensive Development Infrastructure**: 
  - Migration to `uv` for fast Python package management
  - Complete CI/CD pipeline with GitHub Actions
  - Automated testing, linting, and type checking
  - Custom slash commands for common development workflows
  - Comprehensive documentation in CLAUDE.md

### Changed
- **Improved Error Handling**: Enhanced storage path resolution with proper environment variable expansion
- **Better Type Safety**: Full mypy compliance with modern Python type annotations
- **Updated Dependencies**: All dependencies updated to latest stable versions

### Fixed
- **Import Resolution**: Fixed module import issues for standalone DXT execution
- **Storage Initialization**: Resolved file system permission issues with configurable storage paths
- **CI Pipeline**: Updated deprecated GitHub Actions to current versions

## [0.1.0] - 2025-06-30

### Added
- **Core Tidal Workflow System**: Initial implementation of rhythmic productivity management
  - `create_tide` tool for starting new tidal workflows (daily, weekly, project, seasonal)
  - `list_tides` tool for viewing all tides with status filtering
  - `flow_tide` tool for starting focused work sessions with intensity levels
- **Natural Tidal Philosophy**: Built around sustainable productivity metaphors
  - Gentle, moderate, and strong flow intensities
  - Natural rhythm tracking and scheduling
  - Historical insight capture and pattern recognition
- **Robust Storage Layer**: File-based JSON storage with atomic operations
  - Configurable storage paths via environment variables
  - Comprehensive data validation with Pydantic models
  - Automatic backup and recovery mechanisms
- **MCP Integration**: Full Model Context Protocol server implementation
  - Async tool handlers with proper error management
  - Rich tool descriptions and schema validation
  - Claude Desktop compatibility and integration
- **Testing Infrastructure**: Comprehensive test suite with >90% coverage
  - Unit tests for all core functionality
  - Integration tests for storage operations
  - Async test support with proper mocking