#!/usr/bin/env python3
"""Privacy-preserving read-only compatibility report for remote Steam Deck testing."""
import importlib.util
import json
import os
import platform
from pathlib import Path

HERE = Path(__file__).resolve().parent

def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def report(home=None, env=None, proc_root=Path("/proc"), uid=None):
    env = os.environ if env is None else env
    home = Path.home() if home is None else home
    prefixes = load("azs_prefixes", "azs-runtime-discovery.py").discover(home, env)
    processes = load("azs_processes", "azs-process-probe.py").probe(proc_root, uid)
    # Do not serialize process IDs, usernames, home paths, app IDs, or raw environment.
    return {
        "schema": 1,
        "platform": platform.system(),
        "architecture": platform.machine(),
        "session": env.get("XDG_SESSION_TYPE", "unknown") if env.get("XDG_SESSION_TYPE") in {"x11", "wayland"} else "unknown",
        "candidate_prefix_count": len(prefixes),
        "candidate_prefix_sources": sorted(set(p["source"] for p in prefixes)),
        "game_process_count": len(processes),
        "game_runtime_hints": sorted(set(p["runtime"] for p in processes)),
        "unique_game_candidate": len(processes) == 1,
        "game_prefix_hint_present": len(processes) == 1 and bool(processes[0]["prefix"]),
        "controller_connection_verified": False,
        "chrono_verified": False,
    }

def main():
    print(json.dumps(report(), indent=2))
    print("Report contains no discovered paths or PIDs. It does not prove game compatibility.")

if __name__ == "__main__":
    main()
