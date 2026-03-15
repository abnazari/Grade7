#!/usr/bin/env python3
"""
Clean all build/ directories in the Grade 3 study guide project.
"""

import os
import shutil
from pathlib import Path

def clean_builds(project_root="."):
    """
    Find and delete contents of all build/ directories.
    
    Args:
        project_root: Root directory to search from (default: current directory)
    """
    project_path = Path(project_root).resolve()
    build_dirs = list(project_path.rglob("build"))
    
    if not build_dirs:
        print("No build/ directories found.")
        return
    
    print(f"Found {len(build_dirs)} build directory(ies):")
    for build_dir in build_dirs:
        print(f"  - {build_dir}")
    
    # Ask for confirmation
    response = input("\nDelete contents? (yes/no): ").strip().lower()
    if response != "yes":
        print("Cancelled.")
        return
    
    # Delete directories
    for build_dir in build_dirs:
        if build_dir.exists() and build_dir.is_dir():
            try:
                shutil.rmtree(build_dir)
                print(f"✓ Deleted {build_dir}")
            except Exception as e:
                print(f"✗ Error deleting {build_dir}: {e}")
    
    print("Done.")

if __name__ == "__main__":
    clean_builds()
