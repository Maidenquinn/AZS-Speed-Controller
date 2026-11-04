#!/usr/bin/env bash
# Experimental same-prefix Proton launch for the existing Win32 controller.
# It is NOT evidence that DLL injection, overlays, or chrono hooks work on Deck.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  azs-proton-controller.sh /absolute/path/to/proton /absolute/path/to/compatdata /absolute/path/to/AZSSpeedController.exe

Important:
  1. Game must be running through the SAME Proton version and compatdata prefix.
  2. The controller and AZSSpeedHook.dll must be together in a writable directory.
  3. This uses Proton's documented 'run' operation; functionality is experimental.
  4. Set STEAM_COMPAT_CLIENT_INSTALL_PATH if Steam is not in a standard location.
  5. Do not use sudo.
EOF
}

if [[ $# -ne 3 ]]; then usage >&2; exit 64; fi
proton=$1
compat=$2
controller=$3

if [[ ! -f "$proton" ]]; then printf 'Proton script missing: %s\n' "$proton" >&2; exit 66; fi
if [[ ! -f "$compat/pfx/system.reg" ]]; then
  printf 'Existing Wine prefix missing: %s/pfx\n' "$compat" >&2
  printf 'Refusing to create or guess a different prefix.\n' >&2
  exit 66
fi
if [[ ! -f "$controller" ]]; then printf 'Controller missing: %s\n' "$controller" >&2; exit 66; fi
hook="$(dirname "$controller")/AZSSpeedHook.dll"
if [[ ! -f "$hook" ]]; then printf 'Companion hook missing: %s\n' "$hook" >&2; exit 66; fi

if [[ -z "${STEAM_COMPAT_CLIENT_INSTALL_PATH:-}" ]]; then
  for candidate in "$HOME/.steam/steam" "$HOME/.local/share/Steam"; do
    if [[ -d "$candidate" ]]; then
      export STEAM_COMPAT_CLIENT_INSTALL_PATH="$candidate"
      break
    fi
  done
fi
if [[ -z "${STEAM_COMPAT_CLIENT_INSTALL_PATH:-}" ]]; then
  printf 'Steam install path not found. Set STEAM_COMPAT_CLIENT_INSTALL_PATH.\n' >&2
  exit 66
fi
if [[ "${AZS_GAME_CONFIRMED:-}" != "1" ]]; then
  printf "%s\n" "Refusing launch: confirm the base game runs and set AZS_GAME_CONFIRMED=1." >&2
  exit 65
fi
export STEAM_COMPAT_DATA_PATH="$compat"

printf '%s\n' 'Experimental Proton launch; the controller may not connect to the game.'
printf '%s\n' 'Do not interpret launch success as verified chrono acceleration.'
exec "$proton" run "$controller"
