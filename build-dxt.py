#!/usr/bin/env python3
"""
Build script to create a DXT package for Tides
"""

import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def build_dxt():
    """Build the DXT package"""
    print("🌊 Building Tides DXT package...")

    # Get the directory containing this script
    root_dir = Path(__file__).parent

    # Create a temporary directory for building
    with tempfile.TemporaryDirectory() as temp_dir:
        build_dir = Path(temp_dir) / "tides-dxt"
        build_dir.mkdir()

        # Copy server files
        print("📁 Copying server files...")
        shutil.copytree(root_dir / "server", build_dir / "server")

        # Copy manifest
        shutil.copy(root_dir / "manifest.json", build_dir / "manifest.json")

        # Copy icon if it exists
        icon_path = root_dir / "icon.png"
        if icon_path.exists():
            shutil.copy(icon_path, build_dir / "icon.png")

        # Create lib directory and install dependencies
        print("📦 Installing dependencies...")
        lib_dir = build_dir / "server" / "lib"
        lib_dir.mkdir()

        # Install dependencies to lib directory
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--target",
                str(lib_dir),
                "mcp>=1.0.0",
                "pydantic>=2.0.0",
                "python-dotenv>=1.0.0",
            ],
            check=True,
        )

        # Create the DXT file
        dxt_path = root_dir / "tides.dxt"
        print(f"📦 Creating DXT package: {dxt_path}")

        with zipfile.ZipFile(dxt_path, "w", zipfile.ZIP_DEFLATED) as dxt:
            # Add all files from build directory
            for file_path in build_dir.rglob("*"):
                if file_path.is_file():
                    arc_name = str(file_path.relative_to(build_dir))
                    dxt.write(file_path, arc_name)

        # Get file size
        size_mb = dxt_path.stat().st_size / (1024 * 1024)
        print(f"✅ DXT package created successfully! Size: {size_mb:.2f} MB")
        print(f"📍 Location: {dxt_path}")


if __name__ == "__main__":
    try:
        build_dxt()
    except Exception as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)
