"""Qualification must reject wrong source pins and incomplete/corrupt installs."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('qualify_fr5', ROOT / 'scripts/qualify_fr5.py')
qualifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qualifier)


class QualificationProvenanceTests(unittest.TestCase):
    def test_wrong_exact_commit_refused(self):
        with patch.object(qualifier.subprocess, 'check_output', return_value='different\n'):
            with self.assertRaisesRegex(RuntimeError, 'exact source commit unavailable'):
                qualifier.exact_commit(Path('/unused'), 'expected')

    def attest(self, mode):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            export = root / 'export'
            installed = root / 'site-packages'
            source = {'sample/__init__.py': b'# exact source\n', 'sample/other.py': b'# required module\n'}
            wheel = root / 'sample.whl'
            with zipfile.ZipFile(wheel, 'w') as archive:
                for name, value in source.items():
                    for destination in (export / 'src' / name, installed / name):
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        destination.write_bytes(value)
                    if mode != 'missing_module' or not name.endswith('other.py'):
                        archive.writestr(name, value)
            if mode == 'corrupt_installed':
                (installed / 'sample/other.py').write_bytes(b'# wrong source\n')
            if mode == 'extra_installed':
                (installed / 'sample/extra.py').write_bytes(b'# untracked\n')

            def output(argv, **kwargs):
                if '-I' in argv:
                    return str(installed) + '\n'
                if 'rev-parse' in argv:
                    return 'exact\n'
                if 'ls-tree' in argv:
                    return ''.join('src/' + name + '\n' for name in source)
                if 'show' in argv:
                    return source[argv[-1].removeprefix('exact:src/')]
                raise AssertionError(argv)

            with patch.object(qualifier.subprocess, 'check_output', side_effect=output):
                return qualifier.attest(root, 'exact', export, wheel, root / 'bin', 'sample')

    def test_complete_exact_install_attests(self):
        self.assertEqual(self.attest('correct')['python_files'], 2)

    def test_missing_source_module_refused(self):
        with self.assertRaisesRegex(RuntimeError, 'Python closure'):
            self.attest('missing_module')

    def test_corrupt_installed_bytes_refused(self):
        with self.assertRaisesRegex(RuntimeError, 'provenance mismatch'):
            self.attest('corrupt_installed')

    def test_extra_installed_module_refused(self):
        with self.assertRaisesRegex(RuntimeError, 'unexpected installed'):
            self.attest('extra_installed')


if __name__ == '__main__':
    unittest.main()
