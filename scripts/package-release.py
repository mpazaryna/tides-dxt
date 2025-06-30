#!/usr/bin/env python3
"""
Automated release packaging script for Tides DXT.
Handles versioning, changelog updates, git tagging, and DXT building.
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


def get_current_version() -> str:
    """Get the current version from manifest.json."""
    manifest_path = Path("manifest.json")
    with open(manifest_path) as f:
        manifest = json.load(f)
    return manifest["version"]


def validate_version(version: str) -> bool:
    """Validate semantic version format."""
    pattern = r"^\d+\.\d+\.\d+$"
    return bool(re.match(pattern, version))


def compare_versions(v1: str, v2: str) -> int:
    """Compare two semantic versions. Returns -1 if v1 < v2, 0 if equal, 1 if v1 > v2."""
    v1_parts = [int(x) for x in v1.split(".")]
    v2_parts = [int(x) for x in v2.split(".")]
    
    for i in range(3):
        if v1_parts[i] < v2_parts[i]:
            return -1
        elif v1_parts[i] > v2_parts[i]:
            return 1
    return 0


def update_manifest_version(new_version: str) -> None:
    """Update the version in manifest.json."""
    manifest_path = Path("manifest.json")
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    manifest["version"] = new_version
    
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")


def update_changelog(new_version: str, release_notes: Optional[str] = None) -> None:
    """Update CHANGELOG.md with the new version."""
    changelog_path = Path("CHANGELOG.md")
    today = datetime.now().strftime("%Y-%m-%d")
    
    with open(changelog_path) as f:
        content = f.read()
    
    # Find the Unreleased section
    unreleased_pattern = r"## \[Unreleased\]\n\n(.*?)(?=## \[|$)"
    match = re.search(unreleased_pattern, content, re.DOTALL)
    
    if match and match.group(1).strip():
        # Move unreleased content to new version
        unreleased_content = match.group(1).strip()
        
        # Create new version section
        new_section = f"## [{new_version}] - {today}\n\n{unreleased_content}\n\n"
        
        # Add release notes if provided
        if release_notes:
            new_section = f"## [{new_version}] - {today}\n\n{release_notes}\n\n{unreleased_content}\n\n"
        
        # Replace content
        new_content = content.replace(
            f"## [Unreleased]\n\n{unreleased_content}",
            f"## [Unreleased]\n\n{new_section}"
        )
    else:
        # No unreleased content, create new section
        new_section = f"## [{new_version}] - {today}\n\n"
        if release_notes:
            new_section += f"{release_notes}\n\n"
        else:
            new_section += "### Changed\n- Version bump\n\n"
        
        new_content = content.replace(
            "## [Unreleased]\n\n",
            f"## [Unreleased]\n\n{new_section}"
        )
    
    with open(changelog_path, "w") as f:
        f.write(new_content)


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command."""
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def check_git_status() -> bool:
    """Check if git working directory is clean."""
    result = run_command(["git", "status", "--porcelain"], check=False)
    return not result.stdout.strip()


def run_tests() -> bool:
    """Run the test suite."""
    print("\n🧪 Running tests...")
    result = run_command(["uv", "run", "pytest"], check=False)
    return result.returncode == 0


def run_linting() -> bool:
    """Run linting checks."""
    print("\n🔍 Running linting...")
    result = run_command(["uv", "run", "ruff", "check", "."], check=False)
    return result.returncode == 0


def run_type_checking() -> bool:
    """Run type checking."""
    print("\n📝 Running type checking...")
    result = run_command(["uv", "run", "mypy", "server/"], check=False)
    return result.returncode == 0


def main():
    """Main release process."""
    print("🌊 Tides DXT Release Packager")
    print("=" * 40)
    
    # Check git status
    if not check_git_status():
        print("❌ Git working directory is not clean. Please commit or stash changes.")
        sys.exit(1)
    
    # Get current version
    current_version = get_current_version()
    print(f"\n📌 Current version: {current_version}")
    
    # Pre-release checks
    print("\n🔍 Running pre-release checks...")
    
    checks = [
        ("Tests", run_tests),
        ("Linting", run_linting),
        ("Type checking", run_type_checking),
    ]
    
    all_passed = True
    for name, check_func in checks:
        if check_func():
            print(f"✅ {name} passed")
        else:
            print(f"❌ {name} failed")
            all_passed = False
    
    if not all_passed:
        response = input("\n⚠️  Some checks failed. Continue anyway? (y/N): ")
        if response.lower() != "y":
            print("Aborted.")
            sys.exit(1)
    
    # Get new version
    print(f"\nEnter new version (current: {current_version})")
    print("Examples: 0.2.1 (patch), 0.3.0 (minor), 1.0.0 (major)")
    new_version = input("New version: ").strip()
    
    if not validate_version(new_version):
        print("❌ Invalid version format. Use semantic versioning (e.g., 1.2.3)")
        sys.exit(1)
    
    if compare_versions(new_version, current_version) <= 0:
        print(f"❌ New version must be greater than current version ({current_version})")
        sys.exit(1)
    
    # Get release notes (optional)
    print("\nEnter additional release notes (optional, press Enter to skip):")
    release_notes = input().strip() or None
    
    # Confirm
    print(f"\n📋 Release Summary:")
    print(f"  Current version: {current_version}")
    print(f"  New version: {new_version}")
    if release_notes:
        print(f"  Release notes: {release_notes}")
    
    response = input("\nProceed with release? (y/N): ")
    if response.lower() != "y":
        print("Aborted.")
        sys.exit(1)
    
    try:
        # Update files
        print("\n📝 Updating files...")
        update_manifest_version(new_version)
        print("✅ Updated manifest.json")
        
        update_changelog(new_version, release_notes)
        print("✅ Updated CHANGELOG.md")
        
        # Git operations
        print("\n📦 Creating git commit and tag...")
        run_command(["git", "add", "manifest.json", "CHANGELOG.md"])
        run_command(["git", "commit", "-m", f"Release v{new_version}"])
        run_command(["git", "tag", "-a", f"v{new_version}", "-m", f"Release v{new_version}"])
        print(f"✅ Created commit and tag v{new_version}")
        
        # Build DXT
        print("\n🏗️  Building DXT package...")
        run_command([sys.executable, "build-dxt.py"])
        
        # Rename with version
        dxt_path = Path("tides.dxt")
        versioned_path = Path(f"tides-v{new_version}.dxt")
        if versioned_path.exists():
            versioned_path.unlink()
        dxt_path.rename(versioned_path)
        print(f"✅ Built {versioned_path}")
        
        # Summary
        print("\n🎉 Release complete!")
        print(f"\n📊 Summary:")
        print(f"  Version: {new_version}")
        print(f"  Tag: v{new_version}")
        print(f"  Package: {versioned_path}")
        print(f"\n📤 Next steps:")
        print(f"  1. Test the package: {versioned_path}")
        print(f"  2. Push to GitHub: git push origin main --tags")
        print(f"  3. Create GitHub release with {versioned_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: {e}")
        print(f"Output: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()