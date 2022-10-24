import importlib.util
import sys
from types import ModuleType


def import_from_filename(filename: str) -> ModuleType:
    """Import a module from a filename."""
    spec = importlib.util.spec_from_file_location("-", filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load settings file.")  # pragma: no cover

    module = importlib.util.module_from_spec(spec)
    sys.modules["module"] = module
    spec.loader.exec_module(module)

    return module
