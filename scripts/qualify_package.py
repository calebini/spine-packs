#!/usr/bin/env python3
"""Build and qualify a local candidate; never publish or accept an existing ledger.

Run with an isolated Python 3.12+ build environment containing build and
hatchling. All subprocess output and disposable integration evidence is retained.
"""
import argparse
from email.parser import BytesParser
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def qualify(args, run):
    env = os.environ.copy()
    for key in ("PYTHONPATH", "PYTHONHOME"):
        env.pop(key, None)
    env.update(PYTHONNOUSERSITE="1", PYTHONDONTWRITEBYTECODE="1",
               SOURCE_DATE_EPOCH="315532800")

    def command(label, argv, cwd=run, timeout=300):
        print(f"{label} (log: {run / (label + '.log')})", flush=True)
        with (run / (label + ".log")).open("x") as log:
            result = subprocess.run([str(x) for x in argv], cwd=cwd, env=env,
                                    stdout=log, stderr=subprocess.STDOUT, timeout=timeout)
        require(result.returncode == 0, f"{label} failed; inspect retained log")

    config = tomllib.loads((ROOT / "pyproject.toml").read_text())
    version = config["project"]["version"]
    save = {"version": version, "python": sys.version,
            "build": importlib.metadata.version("build"),
            "hatchling": importlib.metadata.version("hatchling"),
            "source": str(ROOT), "qualification": "local-candidate-not-a-release"}
    (run / "environment.json").write_text(json.dumps(save, indent=2) + "\n")
    assets = run / "assets"
    # Default build creates the sdist, then builds the wheel FROM that sdist.
    command("build-from-sdist", [sys.executable, "-m", "build", "--no-isolation",
                                  "--outdir", assets, ROOT])
    wheel = assets / f"spine_packs-{version}-py3-none-any.whl"
    sdist = assets / f"spine_packs-{version}.tar.gz"
    require(wheel.is_file() and sdist.is_file(), "expected wheel and sdist missing")
    expected = {"spine_packs/" + p.name: p.read_bytes()
                for p in (ROOT / "src/spine_packs").glob("*.py")}
    schemas = {p.name: p.read_bytes() for p in (ROOT / "contracts/schemas").glob("*.schema.json")}
    expected.update({"spine_packs/_schemas/" + name: value for name, value in schemas.items()})
    with zipfile.ZipFile(wheel) as archive:
        entries = archive.namelist()
        require(len(entries) == len(set(entries)), "duplicate wheel members")
        info = f"spine_packs-{version}.dist-info/"
        metadata = {info + name for name in (
            "METADATA", "WHEEL", "RECORD", "entry_points.txt", "licenses/LICENSE")}
        require(set(entries) == set(expected) | metadata, "unexpected or missing wheel members")
        for name, value in expected.items():
            require(archive.read(name) == value, f"packaged bytes differ: {name}")
        package_metadata = BytesParser().parsebytes(archive.read(info + "METADATA"))
        require(package_metadata["Version"] == version, "incorrect packaged version")
        require(package_metadata["License-Expression"] == "MIT", "incorrect packaged license")
        require(package_metadata.get_all("License-File") == ["LICENSE"], "incorrect license file metadata")
        require(archive.read(info + "licenses/LICENSE") == (ROOT / "LICENSE").read_bytes(),
                "packaged license differs from source")
        require(not package_metadata.get_all("Requires-Dist"), "runtime dependency added")

    command("build-direct-wheel", [sys.executable, "-m", "build", "--no-isolation", "--wheel",
                                    "--outdir", run / "direct", ROOT])
    require(wheel.read_bytes() == (run / "direct" / wheel.name).read_bytes(),
            "sdist-built wheel differs from directly built wheel")

    extracted = run / "sdist"
    extracted.mkdir()
    source_members = {"src/" + name: value for name, value in expected.items()
                      if "/_schemas/" not in name}
    source_members.update({"contracts/schemas/" + name: value for name, value in schemas.items()})
    for name in (".gitignore", "pyproject.toml", "README.md", "LICENSE", "docs/releases.md",
                 "docs/local-qualification.md",
                 "tests/integration/test_local_spine.py",
                 "tests/fixtures/pack-manifest/positive/medical_and_lesson.json"):
        source_members[name] = (ROOT / name).read_bytes()
    with tarfile.open(sdist) as archive:
        files = [m for m in archive.getmembers() if m.isfile()]
        prefix = f"spine_packs-{version}/"
        require({m.name for m in files} == {prefix + n for n in source_members} | {prefix + "PKG-INFO"},
                "unexpected or missing sdist files")
        require(len(files) == len(source_members) + 1, "duplicate sdist members")
        require(all(m.isfile() or m.isdir() for m in archive.getmembers()), "sdist links forbidden")
        for name, value in source_members.items():
            require(archive.extractfile(prefix + name).read() == value, f"sdist bytes differ: {name}")
        archive.extractall(extracted, filter="data")

    clean = run / "installed"
    command("create-clean-environment", [sys.executable, "-m", "venv", clean])
    python = clean / "bin/python"
    cli = clean / "bin/spine-packs"
    command("install-wheel", [python, "-m", "pip", "install", "--no-index", "--no-deps", wheel])
    command("pip-check", [python, "-m", "pip", "check"])
    command("installed-help", [cli, "--help"])
    command("module-help", [python, "-I", "-m", "spine_packs", "--help"])
    command("installed-integration", [python, "-I", extracted / f"spine_packs-{version}" /
            "tests/integration/test_local_spine.py", "--installed",
            "--spine-command", args.spine_command.resolve(strict=True),
            "--spine-ledger-migrate", args.spine_ledger_migrate.resolve(strict=True),
            "--evidence-parent", run], timeout=900)
    # Emit release checksums only after every local qualification gate passed.
    checksums = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n"
                        for p in sorted((wheel, sdist)))
    (assets / "SHA256SUMS").write_text(checksums)
    (run / "PASS.json").write_text(json.dumps({"passed": True, "assets": str(assets)}) + "\n")
    print(f"Local candidate qualified; nothing published. Assets: {assets}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spine-command", required=True, type=Path)
    parser.add_argument("--spine-ledger-migrate", required=True, type=Path)
    parser.add_argument("--evidence-parent", type=Path, default=Path(tempfile.gettempdir()))
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        parser.error("qualification tooling requires Python 3.12+; installer minimum remains 3.11")
    run = Path(tempfile.mkdtemp(prefix="spine-packs-package-", dir=args.evidence_parent)).resolve()
    print(f"Private package qualification evidence: {run}", flush=True)
    try:
        qualify(args, run)
    except Exception as error:
        print(f"Qualification failed: {error}. Evidence retained: {run}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
