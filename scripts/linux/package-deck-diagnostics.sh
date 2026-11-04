#!/usr/bin/env bash
# Build a portable, source-only diagnostic ZIP. No binaries or game files.
set -euo pipefail
cd "$(dirname "$0")/../.."
out="${1:-dist}"
mkdir -p "$out"
out="$(cd "$out" && pwd)"
stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT
mkdir -p "$stage/AZS-Deck-Diagnostics/scripts/linux" "$stage/AZS-Deck-Diagnostics/docs"
cp scripts/linux/azs-runtime-discovery.py scripts/linux/azs-process-probe.py scripts/linux/azs-compat-report.py scripts/linux/azs-launch-log-summary.py scripts/linux/azs-connection-preflight.py "$stage/AZS-Deck-Diagnostics/scripts/linux/"
cp docs/STEAM-DECK-GAME-STARTUP.md docs/STEAM-DECK-REPORT.md docs/LINUX-CONNECTION-PREFLIGHT.md "$stage/AZS-Deck-Diagnostics/docs/"
cat > "$stage/AZS-Deck-Diagnostics/README.txt" <<'EOF'
AZS Steam Deck diagnostics - PRE-RECETTE ONLY
No game files, Windows binaries, hooks or controller included.
1. Open Konsole in the extracted folder (Desktop Mode).
2. Launch the base game WITHOUT Speed Controller if possible.
3. Run: python3 scripts/linux/azs-compat-report.py
4. Share the printed report with the maintainer.
5. If the game will not launch, read docs/STEAM-DECK-GAME-STARTUP.md.
No sudo, no installations, no prefix deletions.
This package DOES NOT accelerate the game.
EOF
(cd "$stage" && zip -q -r "$out/AZS-Deck-Diagnostics.zip" AZS-Deck-Diagnostics)
sha256sum "$out/AZS-Deck-Diagnostics.zip" > "$out/AZS-Deck-Diagnostics.zip.sha256"
echo "Created $out/AZS-Deck-Diagnostics.zip"
