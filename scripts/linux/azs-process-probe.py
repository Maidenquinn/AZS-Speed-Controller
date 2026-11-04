#!/usr/bin/env python3
"""Read-only Linux /proc probe. Never attaches to or modifies processes."""
import argparse
import json
import os
from pathlib import Path

TARGET = "azerothsurvivors.exe"

def _read_nulls(path):
    try:
        return [v.decode("utf-8", "replace") for v in path.read_bytes().split(b"\0") if v]
    except (OSError, PermissionError):
        return []

def _environment(path):
    pairs = _read_nulls(path)
    result = {}
    for pair in pairs:
        key, sep, value = pair.partition("=")
        if sep and key in {"STEAM_COMPAT_DATA_PATH", "WINEPREFIX", "STEAM_COMPAT_CLIENT_INSTALL_PATH", "SteamAppId", "STEAM_COMPAT_APP_ID"}:
            result[key] = value
    return result

def _matches(args):
    # Require an exact executable basename, not substring matching in arbitrary args.
    # Wine may expose the Windows exe as argv[0] or after a wine/preloader command.
    for arg in args[:3]:
        normalized = arg.replace("\\", "/").rstrip("/").lower()
        if normalized.rsplit("/", 1)[-1] == TARGET:
            return True
    return False

def probe(proc_root=Path("/proc"), uid=None):
    if uid is None:
        uid = os.getuid()
    results = []
    try:
        entries = list(proc_root.iterdir())
    except OSError:
        return results
    for node in entries:
        if not node.name.isdecimal():
            continue
        try:
            if node.stat().st_uid != uid:
                continue
        except OSError:
            continue
        args = _read_nulls(node / "cmdline")
        if not _matches(args):
            continue
        env = _environment(node / "environ")
        # This is a hint only: runtime/prefix association still requires verification.
        results.append({"pid": int(node.name), "prefix": env.get("STEAM_COMPAT_DATA_PATH") or env.get("WINEPREFIX"), "runtime": "proton" if env.get("STEAM_COMPAT_DATA_PATH") else ("wine" if env.get("WINEPREFIX") else "unknown"), "steam_app_id": env.get("SteamAppId") or env.get("STEAM_COMPAT_APP_ID")})
    return sorted(results, key=lambda x: x["pid"])

def main():
    parser = argparse.ArgumentParser(description="Read-only process probe for Azeroth Survivors")
    parser.add_argument("--json", action="store_true", help="Private output: may contain filesystem paths")
    args = parser.parse_args()
    matches = probe()
    if args.json:
        print(json.dumps({"schema": 1, "processes": matches}, indent=2))
        return
    print(f"Candidate game processes: {len(matches)}")
    for match in matches:
        print(f"  PID {match['pid']}: {match['runtime']}; prefix {'available' if match['prefix'] else 'unknown'}")
    if len(matches) != 1:
        print("Automatic connection is blocked: require exactly one candidate.")
    else:
        print("Single candidate found. Prefix and Windows-side process visibility still require verification.")
    print("This tool never opens game memory or injects code.")

if __name__ == "__main__":
    main()
