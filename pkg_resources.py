"""Lightweight pkg_resources shim.

Implements only the two deprecated 'Resource Manager' helpers used by
MultiworldGG worlds (resource_listdir, resource_isdir), backed by
importlib.resources. Importing this module shadows setuptools'
pkg_resources at runtime - that is intentional and contained.
"""
from __future__ import annotations

import importlib.resources
from importlib.resources.abc import Traversable

__all__ = ["resource_listdir", "resource_isdir"]


def _node(package: str, resource_name: str) -> Traversable:
    root = importlib.resources.files(package)
    return root.joinpath(resource_name) if resource_name else root


def resource_listdir(package: str, resource_name: str) -> list[str]:
    return [entry.name for entry in _node(package, resource_name).iterdir()]


def resource_isdir(package: str, resource_name: str) -> bool:
    return _node(package, resource_name).is_dir()
