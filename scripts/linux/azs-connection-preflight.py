#!/usr/bin/env python3
"""Fail-closed, read-only preflight for an experimental Proton controller launch."""
import argparse
import importlib.util
import json
import os
from pathlib import Path

def load_probe():
    path = Path(__file__).resolve().with_name("azs-process-probe.py")
    spec = importlib.util.spec_from_file_location("azs_process_probe", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def check(compatdata, proc_root=Path("/proc"), uid=None):
    compatdata = Path(compatdata).expanduser().resolve()
    if not (compatdata / "pfx").is_dir():
        return {"ok": False, "reason": "missing_prefix"}
    processes = load_probe().probe(proc_root, uid)
    if not processes:
        return {"ok": False, "reason": "game_not_detected"}
    if len(processes) != 1:
        return {"ok": False, "reason": "ambiguous_game_process"}
    game = processes[0]
    if game["runtime"] != "proton" or not game["prefix"]:
        return {"ok": False, "reason": "proton_prefix_unknown"}
    try:
        detected = Path(game["prefix"]).expanduser().resolve(strict=True)
    except OSError:
        return {"ok": False, "reason": "detected_prefix_missing"}
    if detected != compatdata:
        return {"ok": False, "reason": "prefix_mismatch"}
    return {"ok": True, "reason": "single_matching_proton_process", "note": "Linux process/prefix match only; Win32 injection not verified"}

def main():
    parser = argparse.ArgumentParser(description="Read-only Proton prefix/game process preflight")
    parser.add_argument("compatdata", type=Path, help="Existing Steam compatibility data directory")
    parser.add_argument("--json", action="store_true", help="Structured result, without private paths")
    args = parser.parse_args()
    result = check(args.compatdata)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(("PASS" if result["ok"] else "BLOCKED") + ": " + result["reason"])
        if result.get("note"):
            print(result["note"])
    raise SystemExit(0 if result["ok"] else 65)

if __name__ == "__main__":
    main()
