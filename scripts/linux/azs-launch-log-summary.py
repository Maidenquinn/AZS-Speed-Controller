#!/usr/bin/env python3
"""Summarize a Proton log locally without exposing private paths or raw lines."""
import argparse
import json
import re
from pathlib import Path

RULES = {
    "missing_dll": re.compile(r"(?:import_dll|library .* not found|failed to load .*\.dll|module .* not found)", re.I),
    "graphics": re.compile(r"(?:vulkan|dxvk|vkd3d|d3d11|d3d12|failed to create.*device)", re.I),
    "wine_prefix": re.compile(r"(?:wine:.*(?:prefix|configuration)|compatdata|wineboot)", re.I),
    "runtime_failure": re.compile(r"(?:unhandled exception|segmentation fault|fatal error|assertion failed)", re.I),
    "architecture": re.compile(r"(?:bad exe format|wrong architecture|win32.*win64|32-bit.*64-bit)", re.I),
}

def summarize(text):
    counts = {key: 0 for key in RULES}
    for line in text.splitlines():
        for key, pattern in RULES.items():
            if pattern.search(line):
                counts[key] += 1
    return {"schema": 1, "categories": counts, "total_lines": len(text.splitlines()), "raw_log_included": False}

def main():
    parser = argparse.ArgumentParser(description="Privacy-safe summary of a local Proton log")
    parser.add_argument("log", type=Path, help="Path to existing Proton log; never uploaded")
    args = parser.parse_args()
    if not args.log.is_file():
        parser.error("Log file not found")
    if args.log.stat().st_size > 30 * 1024 * 1024:
        parser.error("Log exceeds 30 MiB safety limit")
    text = args.log.read_text(encoding="utf-8", errors="replace")
    print(json.dumps(summarize(text), indent=2))
    print("Category counts are clues, not a diagnosis. Do not share the raw log without reviewing it.")

if __name__ == "__main__":
    main()
