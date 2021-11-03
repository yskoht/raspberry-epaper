import os

import toml

pkg_dir = os.path.join(os.path.dirname(__file__), "..")

t = toml.load(os.path.join(pkg_dir, "pyproject.toml"))
__version__ = t["tool"]["poetry"]["version"]
