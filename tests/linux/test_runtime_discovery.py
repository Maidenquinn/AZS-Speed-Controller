import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/linux/azs-runtime-discovery.py"
spec = importlib.util.spec_from_file_location("azs_runtime_discovery", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class DiscoveryTests(unittest.TestCase):
    def test_empty_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(mod.discover(Path(tmp), {}), [])

    def test_steam_prefix(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            pfx = home / ".local/share/Steam/steamapps/compatdata/12345/pfx"
            pfx.mkdir(parents=True)
            (pfx / "system.reg").write_text("test")
            found = mod.discover(home, {})
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0]["source"], "steam")
            self.assertEqual(found[0]["compatdata"], str(pfx.parent))

    def test_deduplicates_steam_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            pfx = home / ".local/share/Steam/steamapps/compatdata/12345/pfx"
            pfx.mkdir(parents=True)
            (pfx / "system.reg").write_text("test")
            found = mod.discover(home, {"STEAM_COMPAT_DATA_PATH": str(pfx.parent)})
            self.assertEqual(len(found), 1)

    def test_explicit_wine_prefix(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            pfx = home / "custom"
            pfx.mkdir()
            (pfx / "system.reg").write_text("test")
            found = mod.discover(home, {"WINEPREFIX": str(pfx)})
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0]["source"], "wine-env")
            self.assertIsNone(found[0]["compatdata"])

    def test_symlink_not_followed(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            outside = home / "outside"
            outside.mkdir()
            (outside / "system.reg").write_text("test")
            root = home / "Games"
            root.mkdir()
            (root / "link").symlink_to(outside, target_is_directory=True)
            self.assertEqual(mod.discover(home, {}), [])

if __name__ == "__main__":
    unittest.main()
