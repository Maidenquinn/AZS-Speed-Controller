#!/usr/bin/env bash
# Ubuntu 24.04 local test launcher; no injection outside the controller.
set -euo pipefail
usage() {
  cat <<'EOF'
Usage: azs-wine-test.sh /path/to/AZSSpeedController.exe [wineprefix]
Place AZSSpeedHook.dll next to the controller.
Run the game in the SAME Wine prefix first. Never use sudo.
AZS_WINE_TEST_DRY_RUN=1 prints configuration without starting Wine.
EOF
}
if [[ $# -lt 1 || $# -gt 2 ]]; then usage >&2; exit 64; fi
controller="$(realpath -e "$1")" || exit 66
prefix="${2:-$HOME/AZS-Testing/wineprefix}"
if [[ ! -f "$controller" || "${controller,,}" != *.exe ]]; then
  echo 'Controller .exe missing' >&2; exit 66
fi
if [[ ! -f "$(dirname "$controller")/AZSSpeedHook.dll" ]]; then
  echo 'AZSSpeedHook.dll must be next to controller' >&2; exit 66
fi
if [[ ! -f "$prefix/system.reg" ]]; then
  echo 'Existing initialized Wine prefix required (run wineboot --init first)' >&2
  exit 66
fi
if ! command -v wine >/dev/null 2>&1; then
  echo 'Wine executable not installed' >&2; exit 69
fi
export WINEPREFIX="$(realpath -e "$prefix")"
echo "Controller: $controller"
echo "Wine prefix: $WINEPREFIX"
echo 'This is an experimental launch; process injection and chrono are not yet verified.'
if [[ "${AZS_WINE_TEST_DRY_RUN:-0}" == "1" ]]; then
  echo 'DRY RUN: Wine was not started.'
  exit 0
fi
exec wine "$controller"
