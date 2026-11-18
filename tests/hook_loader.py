"""Load project hook modules by file path."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".github" / "hooks" / "scripts"

if str(HOOKS) not in sys.path:
    sys.path.insert(0, str(HOOKS))


def load_hook(module_name: str):
    path = HOOKS / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hook_script(module_name: str) -> Path:
    return HOOKS / f"{module_name}.py"
