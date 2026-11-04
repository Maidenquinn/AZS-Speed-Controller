import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/linux/azs-process-probe.py"
spec = importlib.util.spec_from_file_location("azs_process_probe", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ProcessProbeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
    def tearDown(self):
        self.tmp.cleanup()
    def add(self, pid, argv, env=b""):
        node = self.root / str(pid)
        node.mkdir()
        (node / "cmdline").write_bytes(b"\0".join(x.encode() for x in argv) + b"\0")
        (node / "environ").write_bytes(env)
    def test_exact_name_only(self):
        self.add(12, ["python", "myazerothsurvivors.exe"])
        self.add(13, ["wine64", "C:\\Games\\AzerothSurvivors.exe"])
        found = mod.probe(self.root, os.getuid())
        self.assertEqual([x["pid"] for x in found], [13])
    def test_ignores_unrelated_arguments(self):
        self.add(42, ["python", "launcher.py", "--title", "AzerothSurvivors.exe"])
        self.assertEqual(mod.probe(self.root, os.getuid()), [])
    def test_proton_hint(self):
        self.add(21, ["Z:\\Games\\AzerothSurvivors.exe"], b"STEAM_COMPAT_DATA_PATH=/tmp/compat\0SteamAppId=123\0")
        result = mod.probe(self.root, os.getuid())[0]
        self.assertEqual(result["runtime"], "proton")
        self.assertEqual(result["prefix"], "/tmp/compat")
        self.assertEqual(result["steam_app_id"], "123")
    def test_no_process(self):
        self.assertEqual(mod.probe(self.root, os.getuid()), [])
    def test_multiple_are_not_silently_selected(self):
        self.add(1, ["AzerothSurvivors.exe"])
        self.add(2, ["AzerothSurvivors.exe"])
        self.assertEqual(len(mod.probe(self.root, os.getuid())), 2)

if __name__ == "__main__":
    unittest.main()
