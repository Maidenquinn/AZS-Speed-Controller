#!/usr/bin/env python3
"""Read-only discovery of possible Wine/Proton prefixes. Python stdlib only."""
import argparse
import json
import os
from pathlib import Path

def candidates(home: Path, env: dict):
    roots = [
        ("steam", home / ".local/share/Steam/steamapps/compatdata"),
        ("steam", home / ".steam/steam/steamapps/compatdata"),
        ("heroic", home / "Games/Heroic/Prefixes"),
        ("lutris", home / "Games"),
        ("bottles", home / ".local/share/bottles/bottles"),
        ("bottles-flatpak", home / ".var/app/com.usebottles.bottles/data/bottles/bottles"),
    ]
    if env.get("WINEPREFIX"):
        roots.insert(0, ("wine-env", Path(env["WINEPREFIX"]).expanduser()))
    if env.get("STEAM_COMPAT_DATA_PATH"):
        roots.insert(0, ("steam-env", Path(env["STEAM_COMPAT_DATA_PATH"]).expanduser()))
    return roots

def inspect_prefix(path: Path):
    if (path / "pfx/system.reg").is_file():
        return path / "pfx", path
    if (path / "system.reg").is_file():
        return path, path
    return None

def discover(home: Path, env: dict, depth: int = 3):
    found = {}
    for source, root in candidates(home, env):
        if not root.is_dir():
            continue
        # Bound traversal; never recurse into Windows drives, symlinks or user files.
        queue = [(root, 0)]
        while queue:
            node, level = queue.pop(0)
            result = inspect_prefix(node)
            if result:
                prefix, compat = result
                key = str(prefix.resolve())
                found.setdefault(key, {"source": source, "prefix": str(prefix), "compatdata": str(compat) if prefix != compat else None})
                continue
            if level >= depth:
                continue
            try:
                children = sorted((p for p in node.iterdir() if p.is_dir() and not p.is_symlink()), key=lambda p: p.name)
            except OSError:
                continue
            # Bound candidate breadth, including huge game folders.
            queue.extend((child, level + 1) for child in children[:200])
    return list(found.values())

def main():
    parser = argparse.ArgumentParser(description="Read-only Wine/Proton prefix inventory")
    parser.add_argument("--json", action="store_true", help="Print machine-readable report (contains local paths; do not share publicly)")
    parser.add_argument("--home", type=Path, default=Path.home(), help=argparse.SUPPRESS)
    args = parser.parse_args()
    results = discover(args.home, os.environ)
    if args.json:
        print(json.dumps({"schema": 1, "candidates": results}, indent=2))
    else:
        print(f"Found {len(results)} candidate Wine/Proton prefixes (not confirmed game matches):")
        for i, item in enumerate(results, 1):
            print(f"  {i}. {item['source']}: {item['prefix']}")
        print("Paths are private; redact them before sharing. No game process was modified.")

if __name__ == "__main__":
    main()
