# Steam Deck / Ubuntu 24.04 port — technical plan

Status: **design and platform probe only**. No Linux or Steam Deck gameplay success claimed.

## Audited baseline (Windows v1.3.2)

- `src/controller.cpp`: Win32 GDI window, process discovery, `CreateRemoteThread(LoadLibraryW)` DLL load, per-PID Win32 file mapping, global hotkeys, INI settings.
- `src/hook.cpp`: MinHook detours of `QueryPerformanceCounter`, `GetTickCount`, `GetTickCount64`, `timeGetTime`; monotonic virtual clocks with speed x1–x25.
- `src/timer_fix.cpp`: PE executable section signature scan; patches the *single* identified Rust simulation sleep call (25 ms) to prevent a chrono cap. It is keyed to Windows x64 byte patterns and is build-sensitive.
- `src/timer_policy.h`: small pure-C++ rate calculation and safety gate.

**Critical distinction:** SteamOS runs the Windows game through Proton/Wine. A native Linux controller cannot reuse the Windows DLL loader, Win32 process mapping or Win32 overlays directly. It must either communicate with a Wine/Proton-side helper or build a new backend. A generic `LD_PRELOAD` speed hook into the Linux Steam process is *not* a valid substitute for a Windows PE application.

## Proposed implementation, priority order

### Deck Phase A: probe / runtime compatibility (this branch)

1. Collect Steam Deck SteamOS version, game launch route (Steam non-Steam shortcut, native Steam game, Heroic, Bottles), Proton build, application path, and Wine prefix; never require sudo.
2. Test a **same-prefix Windows bridge**: run the existing Windows controller and hook under precisely the game's Proton/Wine prefix. If game and controller share the same Wine server and architecture, Win32 process discovery and file mapping *may* operate without a native rewrite.
3. Gate expected capability: `classic clocks` vs `chrono scan armed` vs `chrono confirmed`. The signature depends on the PE game version; do not treat `Connected` as proof the chrono fix is active.
4. Verify ×1, ×2, ×5, ×10 and ×25, timer progression, input/focus, pause, game quit/relaunch, and reliable return to ×1 before declaring success.

### Deck Phase B: usability, after probe

- Steam Deck Desktop Mode launcher and clear terminal errors; preserve compatibility with immutable SteamOS base system.
- Access from Gaming Mode through a separate Steam shortcut only after Proton launch/prefix behavior is verified; prefer in-game controller-supported control or Steam Input bindings.
- Decide whether the Win32 overlay remains usable or to replace it with a Linux companion UI communicating with a Windows-prefix bridge. Do not promise a native Wayland overlay without testing gamescope.
- Avoid privileged injection, protected-process bypass, disabling security features, or modifications to the game's installed files.

### Ubuntu 24.04 Phase C

- Reuse Deck/Wine strategy when the game is run via Wine or Proton. Validate system Wine separately from Steam Proton; distinct prefixes and Wine servers must not silently be mixed.
- Test Wayland/X11, app focus and global shortcuts. Require no systemwide environment overrides or broad `ptrace` permission changes.

## Engineering gates

- G0: inspect and document executable architecture and runtime. **Done (source inspection only)**.
- G1: standalone, non-invasive prefix/runtime probe. **Planned**.
- G2: one shared-prefix launch path produces a visible connected state. **Not validated**.
- G3: simulation + clock accuracy confirmed at x1/x2/x5/x10/x25 on Deck. **Not validated**.
- G4: proper close, crash recovery, reconnection and Deck sleep/resume. **Not validated**.
- G5: GUI/Steam Input ergonomics and Ubuntu testing. **Not validated**.
- G6: release packaging, CI cross-build checks, security scan, documentation, and full regression. **Not validated**.

## Release policy

Keep this branch isolated. Keep any PR in Draft until the Deck acceptance matrix, Linux build checks, security review and Windows regressions are complete. **Never merge without explicit maintainer approval.**
