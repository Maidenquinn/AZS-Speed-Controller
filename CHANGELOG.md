## 1.3.2 — Chrono signature scan for 0.139+ (2026-11-02)

- Replace the fixed 0.127.0 executable hash/PE gate with a signature scan of the
  loaded game image: locate `xor ecx / mov edx, 25_000_000 / call` and the Rust
  sleep prologue, then scale only that wait with the selected speed.
- Survives Azeroth Survivors **0.139.0** and later builds that keep the same
  simulation-wait pattern; status shows Chrono armed / call observed / unavailable.
- Maintainer confirmed run-timer acceleration beyond ×5 on the current 0.139 client.
- Classic QPC/GetTickCount hooks remain; UI version label set to v1.3.2.

## 1.3.1 — Chrono fix for 0.127.0 (2026-10-29)

- Scale the local simulation wait with the selected speed on a pinned 0.127.0 EXE.
- Overlay status for chrono armed / call observed / unavailable.
- Superseded for newer clients by 1.3.2 signature scanning.

## Unreleased — GitHub preparation after v1.3.0-rc1 Windows test

- Preserve saved shortcut assignments when registration fails.
- Free remote DLL path allocation when the remote loader has completed, even on failure.
- Mark the hook ready only when all four clock hooks are installed and enabled.
- Add proposed MIT license, third-party notices, issue templates and GitHub publishing guide.
- Include MinHook license in the binary package.
- **Not yet rebuilt or runtime-tested on Windows; previous RC1 binary results do not validate these edits.**

## 1.3.0-rc1 — Release preparation (unverified)

- Resolve the companion DLL relative to the controller executable instead of the process working directory.
- Update packaging version and produce a SHA-256 checksum file.
- Extend Windows CI to produce the portable candidate ZIP and checksum artifact.
- Add release gate and documentation updates.
- Windows compilation, runtime behavior, and translation quality require validation.

## 1.2.3 — UI refresh and repository preparation (candidate)

- Refresh all open owner-drawn windows immediately on language change.
- Clear transient shortcut feedback when switching locale.
- Add release checklist and Windows build CI template.
- Move historical README versions into docs/history.
- Source-only candidate; MSVC build and runtime tests pending.

## [1.2.2] - Source candidate (unreleased)

- Localize shortcut editor and speed-profile panel in all 14 supported languages.
- Fix source declaration order for utility-window rendering functions.
- Save the applied speed (rather than the inactive custom slider value) on profile right-click.
- Add source audit, localization notes, and updated build/release documentation.
- No Windows build or runtime verification performed in this environment.

# Changelog

## [1.2.1] - Source candidate (unreleased)
- Added remappable shortcuts for all supported actions, with INI persistence and collision checks.
- Added three persistent speed profiles and an in-app profiles panel.
- Added shortcuts/profiles access from settings and overlay context menu.
- Removed redundant F12 shortcut; retained F6 → ×1.
- Updated CMake version and release ZIP name; added GitHub-ready documentation and ignore rules.
- **Unverified**: Windows build and game runtime tests are required before release.

## [1.2.0]
- Added a gear settings icon and version label; compact/hide functionality.

## [1.1.x]
- Opacity, custom speed up to ×25, translations, dropdown, lock position, always-on-top, reconnect handling.
