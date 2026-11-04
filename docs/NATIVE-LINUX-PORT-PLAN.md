# Native Linux / SteamOS port — primary target

## Product contract
- Native Linux Azeroth Survivors must be controlled by a native Linux executable. Wine and Proton must **not** be required.
- Steam Deck/SteamOS is priority; Ubuntu 24.04 x86_64 is the first local development and test environment.
- Existing Windows controller stays supported and unchanged.
- Proton/Windows-game compatibility is an optional separate backend, not the primary deliverable.

## Technical boundary
The current Windows design injects a Win32 DLL and hooks Windows time APIs. These hooks cannot affect a native Linux game process. Reusing the Windows controller under Wine does not solve native Linux support.

## Investigation before implementation
1. Obtain and inventory the Linux game distribution, executable architecture, runtime dependencies, graphics backend, and whether it is a Unity/Mono, IL2CPP, native, or other engine. Do not assume.
2. Identify the actual time sources used by the native executable (e.g., clock_gettime, SDL, engine-specific clocks). Validate using symbols, read-only tracing and controlled experiments.
3. Choose an engine-compatible, process-scoped speed backend. Evaluate a launcher with scoped interposition only when the dynamic linker and time source support it; otherwise investigate an explicitly versioned game-specific backend.
4. Keep real time and simulated time separated where necessary to preserve input, audio, rendering, networking, and in-game chrono.
5. Build a native UI/CLI that can report attached/offline/unsupported and reset to x1. Never claim speed or chrono correctness without measurement.
6. Ship distinct x86_64 Linux and SteamOS bundles only after automated tests and hardware testing. Avoid root, global clock changes, kernel modifications, and altering game files.

## Acceptance gates
- Native Linux executable starts without Wine/Proton.
- Game starts independently on Ubuntu.
- Controller targets only the selected game process and handles process exit safely.
- x1, x2, x5, x10, x15, x25 have measured behavior; timer follows intended simulation-time policy.
- Steam Deck Desktop/Gaming Mode and hardware input remain a separate hardware acceptance gate.
- No merge into main until user approval.

## Status
Planning and feasibility only. Native game executable not yet inspected; native hooks/backend not yet implemented.
