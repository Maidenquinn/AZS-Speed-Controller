import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/linux/azs-connection-preflight.py"
spec = importlib.util.spec_from_file_location("azs_preflight", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.compat = self.root / "compat"
        (self.compat / "pfx").mkdir(parents=True)
        self.proc = self.root / "proc"
        self.proc.mkdir()
    def tearDown(self):
        self.temp.cleanup()
    def game(self, pid, compat=None, executable="AzerothSurvivors.exe"):
        node = self.proc / str(pid)
        node.mkdir()
        (node / "cmdline").write_bytes(executable.encode() + b"\0")
        env = b"" if compat is None else ("STEAM_COMPAT_DATA_PATH=" + str(compat)).encode() + b"\0"
        (node / "environ").write_bytes(env)
    def test_no_game_fails_closed(self):
        self.assertEqual(mod.check(self.compat, self.proc, os.getuid())["reason"], "game_not_detected")
    def test_matching_game(self):
        self.game(100, self.compat)
        self.assertTrue(mod.check(self.compat, self.proc, os.getuid())["ok"])
    def test_other_prefix_rejected(self):
        other = self.root / "other"
        other.mkdir()
        self.game(100, other)
        self.assertEqual(mod.check(self.compat, self.proc, os.getuid())["reason"], "prefix_mismatch")
    def test_multiple_games_rejected(self):
        self.game(100, self.compat)
        self.game(101, self.compat)
        self.assertEqual(mod.check(self.compat, self.proc, os.getuid())["reason"], "ambiguous_game_process")
    def test_missing_prefix_rejected(self):
        self.assertEqual(mod.check(self.root / "missing", self.proc, os.getuid())["reason"], "missing_prefix")
    def test_wine_without_proton_hint_rejected(self):
        self.game(100)
        self.assertEqual(mod.check(self.compat, self.proc, os.getuid())["reason"], "proton_prefix_unknown")

if __name__ == "__main__":
    unittest.main()
