# Read-only game process probe

Run `python3 scripts/linux/azs-process-probe.py` while the game is running. It scans readable `/proc/<pid>/cmdline` and a **small allowlist** of environment keys for processes owned by the current user. No root, ptrace, process memory access, DLL injection, or persistent changes.

This is **heuristic**. Wine/Proton may expose the Windows executable under different Linux process names/argv layouts. A missing match does not mean the game is absent; an exact argv match does not establish that the Windows-side controller can see it. If multiple matches exist, automatic selection must be blocked. Some /proc environments restrict access, so unknown is an expected result.

The normal output intentionally omits paths and Steam IDs. `--json` contains local paths and should not be shared publicly.

Next gate: correlate a single Linux process with the same Wine server/prefix and prove the Win32 controller's game enumeration, mapping and hooks. Do not promise working x25 until real game and chrono measurements are captured.
