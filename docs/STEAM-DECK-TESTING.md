# Steam Deck / Ubuntu test protocol (not yet validated)

## First run — safe diagnostics

In Steam Deck Desktop Mode (Konsole) or Ubuntu 24.04 Terminal:

```bash
bash scripts/linux/azs-proton-diagnostics.sh
```

The script checks OS, architecture, active desktop session, tooling and candidate Proton directories. It does not access game memory, change processes, install packages, require admin rights, or automatically discover game directories.

## Why not run the Windows controller as a separate Steam shortcut?

Even if Proton launches `AZSSpeedController.exe`, a **different Wine prefix/server** can isolate it from `AzerothSurvivors.exe`. In that case the Windows process enumeration and per-PID mapping will not connect. The Windows controller also has a Win32 GDI overlay whose behavior in gamescope is unverified.

No official Deck installer or launch command should be published until the specific game launch route is known and a shared-prefix process probe is successful. Do not use `sudo`, root-owned Steam directories, global `LD_PRELOAD`, or blanket `ptrace_scope` changes.

## Manual acceptance grid

| Case | Desktop Mode | Gaming Mode | Ubuntu 24.04 |
| --- | --- | --- | --- |
| Detects game without wrong-process match | Pending | Pending | Pending |
| Connected / timer signature status truthful | Pending | Pending | Pending |
| x1 / x2 / x5 / x10 / x25 | Pending | Pending | Pending |
| Chrono accelerates at x10 and x25 | Pending | Pending | Pending |
| Overlay visible and input accessible | Pending | Pending | Pending |
| Close controller restores x1 | Pending | Pending | Pending |
| Game restart reattaches | Pending | Pending | Pending |
| Device sleep/resume safely reconnects | Pending | Pending | N/A |
| No root privileges or permanent system patch | Pending | Pending | Pending |

Capture runtime versions and outputs locally, redact personal filesystem details, and record actual measured game time vs wall time for a 30-second stable interval at each speed. Mark unstable speeds as experimental.
