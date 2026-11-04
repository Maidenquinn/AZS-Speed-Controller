import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/linux/azs-launch-log-summary.py"
spec = importlib.util.spec_from_file_location("azs_log_summary", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class LogSummaryTests(unittest.TestCase):
    def test_categories_and_redaction(self):
        secret = "/home/private-person/Games/AzerothSurvivors.exe"
        result = mod.summarize(f"wine: configuration in {secret}\nUnhandled exception at {secret}\nDXVK Vulkan error")
        self.assertEqual(result["categories"]["runtime_failure"], 1)
        self.assertEqual(result["categories"]["graphics"], 1)
        self.assertEqual(result["categories"]["wine_prefix"], 1)
        self.assertNotIn(secret, json.dumps(result))
        self.assertFalse(result["raw_log_included"])
    def test_empty(self):
        self.assertEqual(mod.summarize("")["total_lines"], 0)

if __name__ == "__main__":
    unittest.main()
