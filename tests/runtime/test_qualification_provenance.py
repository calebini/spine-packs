"""Qualification must reject wrong source pins and incomplete/corrupt installs."""
import importlib.util
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('qualify_fr5', ROOT / 'scripts/qualify_fr5.py')
qualifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qualifier)
fr2_spec = importlib.util.spec_from_file_location('qualify_fr2', ROOT / 'scripts/qualify_fr2.py')
fr2 = importlib.util.module_from_spec(fr2_spec)
fr2_spec.loader.exec_module(fr2)


class QualificationProvenanceTests(unittest.TestCase):
    def test_replacement_refs_cannot_substitute_pinned_export_or_attestation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); repo = root / 'git'; repo.mkdir()
            env = dict(PATH=os.environ['PATH'], GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null',
                GIT_AUTHOR_NAME='Qualification fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                GIT_COMMITTER_NAME='Qualification fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
            def git(*args, data=None):
                return subprocess.check_output(['git', '-C', str(repo), *args], input=data, env=env)
            git('init', '--quiet', '--initial-branch=main')
            def commit(value):
                blob = git('hash-object', '-w', '--stdin', data=value).decode().strip()
                tree = git('mktree', data=f'100644 blob {blob}\t__init__.py\n'.encode()).decode().strip()
                for name in ('sample', 'src'):
                    tree = git('mktree', data=f'040000 tree {tree}\t{name}\n'.encode()).decode().strip()
                return git('commit-tree', tree, data=b'synthetic provenance fixture\n').decode().strip()
            original = b'# exact original\n'; substituted = b'# replacement content\n'
            pin = commit(original); replacement = commit(substituted)
            git('replace', pin, replacement)
            self.assertEqual(git('rev-parse', pin + '^{commit}').decode().strip(), pin)
            self.assertEqual(git('show', pin + ':src/sample/__init__.py'), substituted)
            qualifier.exact_commit(repo, pin)
            for module in (qualifier, fr2):
                self.assertEqual(subprocess.check_output(module.pinned_git(repo, 'show',
                    pin + ':src/sample/__init__.py'), env=env), original)
            archive = root / 'export.tar'
            subprocess.check_call(qualifier.pinned_git(repo, 'archive', '--format=tar', '--output', str(archive), pin), env=env)
            export = root / 'export'; export.mkdir()
            with tarfile.open(archive) as tar: tar.extractall(export, filter='data')
            self.assertEqual((export / 'src/sample/__init__.py').read_bytes(), original)
            installed = root / 'installed'; (installed / 'sample').mkdir(parents=True)
            wheel = root / 'sample.whl'
            actual_output = subprocess.check_output
            def output(argv, **kwargs):
                if argv[0] == str(root / 'bin/python'): return str(installed) + '\n'
                return actual_output(argv, **kwargs)
            for value in (original, substituted):
                with zipfile.ZipFile(wheel, 'w') as package: package.writestr('sample/__init__.py', value)
                (installed / 'sample/__init__.py').write_bytes(value)
                (export / 'src/sample/__init__.py').write_bytes(value)
                with patch.object(qualifier.subprocess, 'check_output', side_effect=output):
                    if value == original:
                        self.assertEqual(qualifier.attest(repo, pin, export, wheel, root / 'bin', 'sample')['python_files'], 1)
                    else:
                        with self.assertRaisesRegex(RuntimeError, 'provenance mismatch'):
                            qualifier.attest(repo, pin, export, wheel, root / 'bin', 'sample')

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
