"""Package resource selection must not silently borrow checkout contracts."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class PackageResourceTests(unittest.TestCase):
    def load_at(self, folder):
        folder.mkdir(parents=True)
        target = folder / "artifacts.py"
        shutil.copyfile(ROOT / "src/spine_packs/artifacts.py", target)
        spec = importlib.util.spec_from_file_location("resource_probe", target)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_source_layout_uses_authoritative_contracts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            module = self.load_at(root / "src/spine_packs")
            self.assertEqual(module.SCHEMA_ROOT, root / "contracts/schemas")

    def test_installed_layout_uses_bundled_schemas(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            package = root / "lib/site-packages/spine_packs"
            module = self.load_at(package)
            self.assertEqual(module.SCHEMA_ROOT, package / "_schemas")

    def test_missing_installed_resources_do_not_fall_back(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            # A tempting nearby contracts directory must never repair a broken wheel.
            shutil.copytree(ROOT / "contracts/schemas", root / "lib/contracts/schemas")
            module = self.load_at(root / "lib/site-packages/spine_packs")
            with self.assertRaises(FileNotFoundError):
                module.EMBEDDED_SCHEMA.read_text()


if __name__ == "__main__":
    unittest.main()
