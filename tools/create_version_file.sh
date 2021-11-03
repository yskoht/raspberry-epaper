#!/bin/sh
version=$(grep '^version = "' pyproject.toml | cut -c 11-)
echo "__version__ = ${version}" > raspberry_epaper/__init__.py
