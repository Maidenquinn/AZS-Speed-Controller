#!/usr/bin/env bash
# Non-invasive Steam Deck / Ubuntu environment report.
# Does not inject code, change a game process, or require root.
set -euo pipefail

say() { printf '%s\n' "$*"; }
command_available() { if command -v "$1" >/dev/null 2>&1; then command -v "$1"; else printf '%s' unavailable; fi; }

say 'AZS Speed Controller - Linux / SteamOS diagnostics'
say 'No changes will be made to your system.'
say ""
say "OS:"
if [[ -r /etc/os-release ]]; then
  # shellcheck disable=SC1091
  source /etc/os-release
  say "  Name: ${PRETTY_NAME:-unknown}"
  say "  ID: ${ID:-unknown}"
else
  say "  /etc/os-release unavailable"
fi
say "Architecture: $(uname -m)"
say "Kernel: $(uname -r)"
say "Session type: ${XDG_SESSION_TYPE:-unknown}"
say "Desktop: ${XDG_CURRENT_DESKTOP:-unknown}"
say "Steam: $(command_available steam)"
say "Wine: $(command_available wine)"
say "Winetricks: $(command_available winetricks)"
say "Protontricks: $(command_available protontricks)"
say "Flatpak: $(command_available flatpak)"
say ""
say 'Candidate Proton installations (names only):'
found=0
for base in "$HOME/.steam/steam/steamapps/common" "$HOME/.local/share/Steam/steamapps/common"; do
  if [[ -d "$base" ]]; then
    while IFS= read -r -d '' path; do
      say "  $(basename "$path")"
      found=1
    done < <(find "$base" -mindepth 1 -maxdepth 1 -type d \( -iname 'Proton*' -o -iname '*SteamLinuxRuntime*' \) -print0 2>/dev/null)
  fi
done
if (( found == 0 )); then say '  None found in standard Steam directories'; fi
say ""
say 'Game-specific runtime and compatibility cannot be inferred from this report.'
say 'Do not post Wine prefixes or game paths publicly if they contain personal names.'
