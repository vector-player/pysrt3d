# pysrt3d package
import sys
from pathlib import Path
import importlib.util

# Try to find the .pyd file
_pyd_paths = [
    Path(__file__).parent / "pysrt3d.cp311-win_amd64.pyd",
    Path(__file__).parent.parent / "build" / "lib.win-amd64-cpython-311" / "Release" / "pysrt3d.cp311-win_amd64.pyd",
    Path(__file__).parent.parent / "build" / "lib.win-amd64-cpython-311" / "pysrt3d.cp311-win_amd64.pyd",
]

_pyd_found = None
for pyd_path in _pyd_paths:
    if pyd_path.exists():
        _pyd_found = pyd_path
        break

if _pyd_found:
    # Load the .pyd file directly using importlib to avoid recursive import
    spec = importlib.util.spec_from_file_location("_pysrt3d_core", str(_pyd_found))
    _pysrt3d_core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_pysrt3d_core)
    # Copy all public attributes to this module's namespace
    for attr in dir(_pysrt3d_core):
        if not attr.startswith('_'):
            setattr(sys.modules[__name__], attr, getattr(_pysrt3d_core, attr))
else:
    raise ImportError("Could not find pysrt3d.pyd file. Please build the package first.")

__version__ = "0.0.0"
