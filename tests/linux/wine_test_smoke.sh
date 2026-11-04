#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/prefix" "$tmp/bin"
: > "$tmp/prefix/system.reg"
: > "$tmp/AZSSpeedController.exe"
: > "$tmp/AZSSpeedHook.dll"
cat > "$tmp/bin/wine" <<'EOF'
#!/bin/sh
echo "mock wine invoked" >&2
exit 0
EOF
chmod +x "$tmp/bin/wine"
PATH="$tmp/bin:$PATH" AZS_WINE_TEST_DRY_RUN=1 bash scripts/linux/azs-wine-test.sh "$tmp/AZSSpeedController.exe" "$tmp/prefix" > "$tmp/out"
grep -q 'DRY RUN' "$tmp/out"
if PATH="$tmp/bin:$PATH" bash scripts/linux/azs-wine-test.sh "$tmp/AZSSpeedController.exe" "$tmp/missing" >"$tmp/out" 2>"$tmp/err"; then
  echo 'FAIL: missing prefix accepted' >&2
  exit 1
fi
grep -q 'Existing initialized Wine prefix required' "$tmp/err"
echo 'Wine launcher smoke: PASS'
