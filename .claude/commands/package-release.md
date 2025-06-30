# Package Release

## Overview
This command automates the release process for Tides DXT, including updating the changelog, version numbers, creating git tags, and building the distribution package.

## Process
The command will:
1. Prompt for the new version number and release type (patch/minor/major)
2. Update CHANGELOG.md with the new version section
3. Update manifest.json with the new version
4. Commit the changes
5. Create a git tag
6. Build the DXT package
7. Display the release summary

## Usage
Run this command when you're ready to create a new release. Make sure all changes are committed before starting.

### Steps:
1. **Version Selection**
   - Ask for the new version number (e.g., 0.2.1, 0.3.0, 1.0.0)
   - Validate it follows semantic versioning

2. **Changelog Update**
   - Move items from [Unreleased] to the new version section
   - Add the current date
   - Prompt for any additional release notes

3. **Manifest Update**
   - Update the version field in manifest.json

4. **Git Operations**
   - Stage CHANGELOG.md and manifest.json
   - Create a commit with message: "Release v{version}"
   - Create an annotated tag: `git tag -a v{version} -m "Release v{version}"`

5. **Build Package**
   - Run `python build-dxt.py`
   - Rename the output file to include version: `tides-v{version}.dxt`

6. **Summary**
   - Display the release summary
   - Show the location of the built package
   - Remind to push tags: `git push origin main --tags`

## Implementation

A release automation script is available at `scripts/package-release.py` that handles all these steps automatically:

```bash
# Run the release script
python scripts/package-release.py

# Or if you prefer
./scripts/package-release.py
```

The script will:
1. Run pre-release checks (tests, linting, type checking)
2. Prompt for the new version number
3. Update manifest.json and CHANGELOG.md
4. Create git commit and tag
5. Build the DXT package with version in filename
6. Provide next steps for pushing to GitHub

## Example Workflow
```bash
# 1. Ensure all changes are committed
git status

# 2. Run the release script
python scripts/package-release.py

# 3. Follow the prompts
# 4. Test the generated DXT package
# 5. Push to GitHub with tags
git push origin main --tags
```

## Pre-release Checklist
- [ ] All tests passing (`uv run pytest`)
- [ ] Linting clean (`uv run ruff check .`)
- [ ] Type checking passes (`uv run mypy server/`)
- [ ] CHANGELOG.md has unreleased changes documented
- [ ] No uncommitted changes (`git status`)