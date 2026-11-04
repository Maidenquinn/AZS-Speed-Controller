import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts/linux"
spec = importlib.util.spec_from_file_location("azs_report", SCRIPTS / "azs-compat-report.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class CompatReportTests(unittest.TestCase):
    def test_private_values_not_exported(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            secret = "private-user-home"
            prefix = home / ".local/share/Steam/steamapps/compatdata/123/pfx"
            prefix.mkdir(parents=True)
            (prefix / "system.reg").write_text("")
            proc = home / "proc"
            game = proc / "100"
            game.mkdir(parents=True)
            (game / "cmdline").write_bytes(b"AzerothSurvivors.exe\0")
            (game / "environ").write_bytes(f"STEAM_COMPAT_DATA_PATH={home}/{secret}\0SteamAppId=7654321\0".encode())
            result = mod.report(home, {"XDG_SESSION_TYPE": "wayland"}, proc, os.getuid())
            encoded = json.dumps(result)
            for forbidden in (tmp, secret, "7654321", '"100"', "AzerothSurvivors.exe"):
                self.assertNotIn(forbidden, encoded)
            self.assertEqual(result["candidate_prefix_count"], 1)
            self.assertEqual(result["game_process_count"], 1)
            self.assertTrue(result["unique_game_candidate"])
            self.assertFalse(result["chrono_verified"])

if __name__ == "__main__":
    unittest.main()
