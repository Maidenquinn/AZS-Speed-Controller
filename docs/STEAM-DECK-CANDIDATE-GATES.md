# Steam Deck functional candidate: acceptance gates

This workflow builds the existing Windows controller and hook DLL on a Windows runner. **A successful build is not a successful Steam Deck test**.

## Gate 1: reproducible binaries
- Windows Release x64 CMake build passes.
- Controller EXE and hook DLL are both present.
- SHA-256 hashes are recorded by the workflow.

## Gate 2: baseline game startup
- The base game launches on the tester's Steam Deck without the controller.
- Proton version, Desktop/Gaming Mode, and launch method are recorded.
- No controller test proceeds while the game itself fails to start.

## Gate 3: same-prefix experimental launch
- Use the exact Proton executable/version and compatdata directory used by the running game.
- Launch the candidate controller with `scripts/linux/azs-proton-controller.sh`.
- If process detection works, set `AZS_STRICT_PREFLIGHT=1` for an additional fail-closed check. If the Linux process is not visible, do not infer a game failure.
- Confirm the controller reports a connected game and the hook mapping status; a visible UI alone is insufficient.

## Gate 4: functional chrono test
- Compare real elapsed wall-clock time with the in-game timer at x1, x2, x5, x10, x15, x25.
- Observe whether simulation speed, UI, audio and chrono remain stable; do not infer success from visual animation alone.
- Record the controller hook state (classic clocks vs chrono armed vs chrono observed).
- Verify reset to x1 and clean exit.

## Gate 5: platform UX
- Verify Desktop Mode and Gaming Mode separately, including gamescope and input controls.
- Confirm no changes to saves or game files.

## Release decision
If Gate 1 passes but Gates 2-5 are unverified, publish only as an **experimental candidate**, not a working Steam Deck release. Keep the PR draft until the user approves.
