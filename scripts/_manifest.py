"""Typed access to the marketplace and plugin manifests.

JSON arrives untyped, so it is parsed and shaped once here rather than leaking
`Any` through every caller.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypedDict, cast

PLUGINS_DIR = "plugins"
MARKETPLACE_PATH = ".claude-plugin/marketplace.json"

# Present on disk but deliberately not registered.
UNREGISTERED: frozenset[str] = frozenset({"product-team"})


class PluginManifest(TypedDict, total=False):
    """A plugin's own `.claude-plugin/plugin.json`."""

    name: str
    version: str
    description: str
    homepage: str
    repository: str | dict[str, str]
    license: str
    keywords: list[str]
    skills: list[str]
    hooks: str


class MarketplaceEntry(TypedDict, total=False):
    """One row of the marketplace registry."""

    name: str
    source: str
    description: str
    version: str
    homepage: str
    category: str


class MarketplaceMetadata(TypedDict, total=False):
    description: str
    version: str


class Marketplace(TypedDict, total=False):
    name: str
    metadata: MarketplaceMetadata
    plugins: list[MarketplaceEntry]


def read_json(path: str | Path) -> Any:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: str | Path, data: object) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        _ = fh.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def load_marketplace(path: str = MARKETPLACE_PATH) -> Marketplace:
    return cast(Marketplace, read_json(path))


def load_plugin(name: str) -> PluginManifest:
    return cast(PluginManifest, read_json(plugin_manifest_path(name)))


def plugin_manifest_path(name: str) -> str:
    return f"{PLUGINS_DIR}/{name}/.claude-plugin/plugin.json"


def entries(marketplace: Marketplace) -> list[MarketplaceEntry]:
    return marketplace.get("plugins", [])


def source_dir(entry: MarketplaceEntry) -> str:
    """Repo-relative directory for a registry entry."""
    return entry.get("source", "").lstrip("./")


def skill_dirs(root: str | Path) -> list[str]:
    """Every directory under root containing a SKILL.md, as posix paths."""
    return sorted(p.parent.as_posix() for p in Path(root).rglob("SKILL.md") if p.is_file())
