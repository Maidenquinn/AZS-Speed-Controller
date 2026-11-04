#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
launcher="$PWD/scripts/linux/azs-proton-controller.sh"
diag="$PWD/scripts/linux/azs-proton-diagnostics.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# A launcher without explicit parameters must fail, without launching anything.
if bash "$launcher" >"$tmp/out" 2>"$tmp/err"; then
  echo 'FAIL: missing arguments accepted' >&2
  exit 1
fi
grep -q 'Usage:' "$tmp/err"

# A non-existent Proton must fail before any execution.
if bash "$launcher" "$tmp/no-proton" "$tmp/no-prefix" "$tmp/no-controller" >"$tmp/out" 2>"$tmp/err"; then
  echo 'FAIL: missing Proton accepted' >&2
  exit 1
fi
grep -q 'Proton script missing' "$tmp/err"

# Fake Proton, real file; missing prefix must be refused.
printf '#!/bin/sh\nexit 99\n' > "$tmp/proton"
if bash "$launcher" "$tmp/proton" "$tmp/no-prefix" "$tmp/no-controller" >"$tmp/out" 2>"$tmp/err"; then
  echo 'FAIL: missing prefix accepted' >&2
  exit 1
fi
grep -q 'Existing Wine prefix missing' "$tmp/err"

# Existing prefix; missing controller must fail.
mkdir -p "$tmp/compat/pfx"
if bash "$launcher" "$tmp/proton" "$tmp/compat" "$tmp/no-controller" >"$tmp/out" 2>"$tmp/err"; then
  echo 'FAIL: missing controller accepted' >&2
  exit 1
fi
grep -q 'Controller missing' "$tmp/err"

# Existing controller; missing hook must fail.
: > "$tmp/AZSSpeedController.exe"
if bash "$launcher" "$tmp/proton" "$tmp/compat" "$tmp/AZSSpeedController.exe" >"$tmp/out" 2>"$tmp/err"; then
  echo 'FAIL: missing DLL accepted' >&2
  exit 1
fi
grep -q 'Companion hook missing' "$tmp/err"

# Mock Proton verifies argument propagation without invoking Wine or touching game processes.
: > "$tmp/AZSSpeedHook.dll"
cat > "$tmp/proton" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
[[ "$1" == run ]]
[[ "$2" == */AZSSpeedController.exe ]]
[[ "$STEAM_COMPAT_DATA_PATH" == */compat ]]
[[ -d "$STEAM_COMPAT_CLIENT_INSTALL_PATH" ]]
EOF
chmod +x "$tmp/proton"
STEAM_COMPAT_CLIENT_INSTALL_PATH="$tmp" bash "$launcher" "$tmp/proton" "$tmp/compat" "$tmp/AZSSpeedController.exe" >"$tmp/out" 2>"$tmp/err"

# Strict preflight must reject launch if no game is detected.
if AZS_STRICT_PREFLIGHT=1 STEAM_COMPAT_CLIENT_INSTALL_PATH="$tmp" bash "$launcher" "$tmp/proton" "$tmp/compat" "$tmp/AZSSpeedController.exe" >"$tmp/out" 2>"$tmp/err"; then
  echo 'FAIL: strict preflight accepted missing game' >&2
  exit 1
fi
grep -q 'BLOCKED: game_not_detected' "$tmp/out"

# Diagnostics must run unprivileged without requiring Steam.
bash "$diag" >"$tmp/diagnostics"
grep -q 'No changes will be made' "$tmp/diagnostics"
echo 'Linux launcher validation and non-invasive diagnostics: PASS'
