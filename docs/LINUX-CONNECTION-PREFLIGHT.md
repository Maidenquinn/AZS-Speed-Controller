# Proton connection preflight (experimental)

Run from the extracted repository root, **with the base game already running**:

```bash
python3 scripts/linux/azs-connection-preflight.py "/absolute/path/to/steamapps/compatdata/APPID"
```

The preflight checks that exactly one readable candidate `AzerothSurvivors.exe` process is found and that its `STEAM_COMPAT_DATA_PATH` resolves to the explicitly selected compatdata directory. It fails closed for zero/multiple processes, missing prefixes, missing environment hints and mismatches.

It is read-only, does not need root and does not perform DLL injection. A PASS is **not** proof that the controller can see the game through Win32 APIs, nor that hooks, speed scaling or the timer fix work.

The Linux `/proc` view of Wine/Proton processes varies. False negatives are expected and should be investigated, **not bypassed by guessing**. This check is currently standalone, not an automatic gate in the existing experimental launcher, to preserve its existing mock smoke tests until integrated end-to-end tests are ready.

Run: `python3 -m unittest discover -s tests/linux -p 'test_*.py' -v`.
