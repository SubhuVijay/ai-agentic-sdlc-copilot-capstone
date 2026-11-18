"""Compatibility wrapper. Prefer scripts/load_user_story.py."""

import runpy
from pathlib import Path

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).with_name("load_user_story.py")), run_name="__main__")
