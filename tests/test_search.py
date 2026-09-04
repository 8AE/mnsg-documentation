"""Run component callback regressions through the installed Docusaurus toolchain."""
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless((ROOT / "node_modules/@babel/parser").is_dir() and shutil.which("node"), "Run npm ci before component search verification.")
class SearchBehaviorTests(unittest.TestCase):
    def test_native_search_navigation_and_keyboard_regressions(self):
        result = subprocess.run(["node", "--test", "tests/search_behaviors.cjs"], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
