import toml

t = toml.load("pyproject.toml")
__version__ = t["tool"]["poetry"]["version"]
