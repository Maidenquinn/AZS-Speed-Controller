# Steam Deck: game does not launch (pre-controller gate)

**User report (2026-11-04):** tester says both Steam and non-Steam/Proton launch methods were attempted and neither opens the game. Exact steps, Proton version and failure symptoms are unknown. This is a *game startup issue*, not yet evidence of a controller defect.

## Safe triage

1. In Desktop Mode, confirm that the downloaded game archive is fully extracted and that the selected shortcut targets the actual `AzerothSurvivors.exe` (not a ZIP, launcher installer, or a different EXE).
2. In the Steam shortcut's **Properties > Compatibility**, select a Proton version deliberately and record its exact name. Avoid changing multiple settings simultaneously.
3. If a non-Steam shortcut, check the shortcut's **Start In** directory points to the folder containing the EXE. Quoting and paths containing spaces matter.
4. Launch the game **without AZS Speed Controller**. Record whether Steam shows Running briefly, whether a black screen appears, or whether an error dialog is displayed.
5. For a Steam-managed Proton launch, set Steam launch options to `PROTON_LOG=1 %command%`, retry once, then restore the original launch options. Steam may write a `steam-<appid>.log` file in the home directory; location depends on the setup.
6. Summarize a local log without disclosing raw paths:
   ```bash
   python3 scripts/linux/azs-launch-log-summary.py /path/to/steam-APPID.log
   ```
7. Send the compatibility report:
   ```bash
   python3 scripts/linux/azs-compat-report.py
   ```

Do **not** run arbitrary internet scripts, disable SteamOS security, use sudo, delete Wine prefixes or game saves, or upload raw logs with personal information.

## Classification

- Game does not start without controller: game/Proton setup issue; **controller integration blocked**.
- Game starts, controller does not detect: process/prefix matching issue.
- Controller connects, speed not applied: Windows hook / Proton behavior issue.
- Speed works, timer does not: Rust simulation-sleep signature/chrono issue.
- Desktop Mode works but Gaming Mode fails: gamescope / input / overlay issue.

The controller cannot be accepted until the base game launches successfully. Keep the PR in Draft.
