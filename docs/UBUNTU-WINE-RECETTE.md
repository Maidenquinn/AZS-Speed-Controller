# Ubuntu 24.04 / VirtualBox: first Wine test

**Experimental only.** This is not yet a functional Steam Deck release.

1. Install Wine and initialize a dedicated prefix:
   ```bash
   mkdir -p "$HOME/AZS-Testing"
   export WINEPREFIX="$HOME/AZS-Testing/wineprefix"
   export WINEARCH=win64
   wineboot --init
   ```
2. Download the `AZS-Windows-Binaries-For-Proton-Candidate` artifact from the successful `Steam Deck controller candidate` GitHub Actions workflow. Extract the two binaries into the same directory.
3. Download or clone the `feat/steamdeck-proton-linux-port` source branch to access the scripts.
4. Launch the controller without the game first, to check whether its UI opens:
   ```bash
   bash scripts/linux/azs-wine-test.sh "$HOME/AZS-Testing/bin/AZSSpeedController.exe" "$HOME/AZS-Testing/wineprefix"
   ```
5. Only if the controller starts, try the base game in **the same prefix**, without controller. Do not infer that game startup is possible in VirtualBox: virtual GPU and Vulkan support are limited.
6. When the game starts independently, repeat the controller launch and record connection, speed and chrono behavior.

**Do not** run as root, change the Windows installation, copy saves unnecessarily, or modify the game's files. The test runner never injects by itself; the Windows controller still implements its original injection behavior.

The Ubuntu Wine launcher is **not** the Proton launcher. Same-prefix Proton testing still requires the exact Steam compatdata and Proton executable.
