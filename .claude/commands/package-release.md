# Package Release

## Overview
This command automates the release process for Tides DXT. When you run this command, I will handle all the release steps including updating the changelog, version numbers, creating git tags, and building the distribution package.

## What I'll Do

When you run `/project:package-release`, I will:

1. **Pre-release Checks**
   - Check git status to ensure working directory is clean
   - Run tests with `uv run pytest`
   - Run linting with `uv run ruff check .`
   - Run type checking with `uv run mypy server/`

2. **Version Management**
   - Read current version from manifest.json
   - Ask you for the new version number
   - Validate it follows semantic versioning (X.Y.Z)
   - Ensure new version is greater than current version

3. **Update Files**
   - Update version in `manifest.json`
   - Update `CHANGELOG.md`:
     - Move content from [Unreleased] to new version section
     - Add current date to version header
     - Ask if you want to add any additional release notes

4. **Git Operations**
   - Stage `manifest.json` and `CHANGELOG.md`
   - Create commit: `git commit -m "Release v{version}"`
   - Create annotated tag: `git tag -a v{version} -m "Release v{version}"`

5. **Build Package**
   - Run `python build-dxt.py`
   - Rename output to include version: `tides-v{version}.dxt`

6. **Final Summary**
   - Show release summary with version, tag, and package location
   - Remind you to push: `git push origin main --tags`
   - Suggest creating a GitHub release

## Usage

Simply run: `/project:package-release`

I'll guide you through the process interactively, asking for:
- New version number
- Additional release notes (optional)
- Confirmation before proceeding

## Requirements

Before running this command:
- Ensure all changes are committed (`git status` should be clean)
- Document any changes in the [Unreleased] section of CHANGELOG.md
- Make sure you're on the main branch

## Example Session

```
You: /project:package-release

Me: I'll help you create a new release for Tides DXT.

First, let me run the pre-release checks...
✅ Git working directory is clean
✅ Tests passed (23 tests)
✅ Linting passed
✅ Type checking passed

Current version: 0.2.0

What should the new version be? (e.g., 0.2.1, 0.3.0, 1.0.0)

You: 0.3.0

Me: Would you like to add any additional release notes beyond what's in [Unreleased]? (optional)

You: Added automated release tooling

Me: Great! Here's what I'll do:
- Update version from 0.2.0 to 0.3.0
- Update CHANGELOG.md with today's date
- Create git commit and tag v0.3.0
- Build tides-v0.3.0.dxt

Proceed? (y/n)

You: y

Me: [executes all steps]

✅ Release v0.3.0 completed successfully!
- Package: tides-v0.3.0.dxt (6.59 MB)
- Tag: v0.3.0

Next steps:
1. Test the package locally
2. Push to GitHub: git push origin main --tags
3. Create GitHub release and upload tides-v0.3.0.dxt
```