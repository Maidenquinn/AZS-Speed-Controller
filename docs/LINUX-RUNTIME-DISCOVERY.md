# Linux runtime discovery — implementation status

The read-only prototype `scripts/linux/azs-runtime-discovery.py` enumerates **candidate prefixes**, not detected Azeroth Survivors instances. It uses only the Python standard library, avoids symlink traversal below search roots, limits depth and breadth, and never launches or injects into a process.

Run:

```bash
python3 scripts/linux/azs-runtime-discovery.py
```

For local debugging only, `--json` prints private filesystem paths. **Do not post the raw JSON publicly.**

Known root conventions include Steam compatibility data, Heroic's common prefix folder, Lutris's common Games folder, Bottles and Bottles Flatpak, plus explicit `WINEPREFIX` / `STEAM_COMPAT_DATA_PATH`. Custom install paths are not automatically covered. A prefix found on disk might be stale or belong to another game. Some Wine prefixes have no `system.reg` until initialized.

## Next integration gate

Correlate an actual running `AzerothSurvivors.exe` with a prefix **without relying on filename alone**. Require an unambiguous match, explicit user confirmation before launch, and a tested bridge mechanism. This discovery script does not authorize arbitrary injection and does not establish Proton compatibility.

Run unit tests:

```bash
python3 -m unittest discover -s tests/linux -p 'test_*.py' -v
```
