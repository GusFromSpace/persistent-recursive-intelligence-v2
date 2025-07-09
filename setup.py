#!/usr/bin/env python3
"""
setup.py for persistent-recursive-intelligence

Backwards compatibility setup.py for older pip versions and build systems
that don't support pyproject.toml. The main configuration is in pyproject.toml.
"""

from setuptools import setup

# Minimal setup.py that defers to pyproject.toml
# This provides backwards compatibility while avoiding duplication
setup()