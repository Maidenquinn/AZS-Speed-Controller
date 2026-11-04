# Remote Steam Deck tester handoff

This is a **remote test protocol**, not a claim of Deck compatibility.

## Tester prerequisites

- Steam Deck in Desktop Mode, with Azeroth Survivors already installed and running via Steam Proton.
- Exact game launch method (non-Steam shortcut, Steam, Heroic, etc.) and Proton version.
- Controller EXE and matching DLL from an official project build; **do not download arbitrary EXEs**.
- A way to send a short report or screenshots privately. No root access, no disabled security tools.

## Step 1 — diagnostics only

Download the source ZIP from the dedicated development branch and run from its extracted root in Konsole:

```bash
bash scripts/linux/azs-proton-diagnostics.sh
```

Send only the OS, architecture, session type, and installed tools. Do not post home-directory paths, Proton prefix contents, account names or personal data.

## Step 2 — developer review

Before giving any game launch command, maintainer checks the launch method, prefix identity and expected Proton path. The experimental launcher requires the **same** prefix and Proton runtime as the running game, and its launch is not proof of functional compatibility.

## Step 3 — gameplay acceptance (after bridge validation)

- x1 baseline and reset; x2, x5, x10, x25.
- Check actual game-world speed *and* game timer, not just controller UI.
- Verify x1 after controller closes, game restart and Deck sleep/resume.
- Check Desktop Mode then Gaming Mode, including gamepad focus and overlay usability.
- Report crash, flicker, audio distortion or incorrect timer; stop on instability.

## Report template

```text
SteamOS version:
Steam Deck model (LCD/OLED):
Desktop or Gaming Mode:
Game version:
How game was installed/launched:
Proton version:
Controller build/commit:
Game detected?:
Connected status:
x1 / x2 / x5 / x10 / x25:
Chrono matches speed?:
Can control from gamepad?:
Close restores x1?:
Crash or other issue:
```

## Release gate

No Steam Deck release until a real Deck tester validates core controls and chrono acceleration. No merge into main without maintainer approval.
