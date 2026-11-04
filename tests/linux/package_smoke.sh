#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
bash scripts/linux/package-deck-diagnostics.sh "$tmp"
test -s "$tmp/AZS-Deck-Diagnostics.zip"
(cd "$tmp" && sha256sum -c AZS-Deck-Diagnostics.zip.sha256)
unzip -Z1 "$tmp/AZS-Deck-Diagnostics.zip" | grep -q '^AZS-Deck-Diagnostics/README.txt$'
if unzip -Z1 "$tmp/AZS-Deck-Diagnostics.zip" | grep -E '\.(exe|dll)$'; then
  echo 'FAIL: executable binaries in diagnostics package' >&2
  exit 1
fi
echo 'Source-only diagnostics package: PASS'
