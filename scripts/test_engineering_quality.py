"""Offline installer/quality-runner acceptance checks for Repo Factory."""
from pathlib import Path
import importlib.util
import json
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import install_engineering_quality as installer


def check(condition, msg):
    if not condition:
        raise AssertionError(msg)


with tempfile.TemporaryDirectory(prefix="factory-quality-") as tmp:
    target = Path(tmp) / "project"
    target.mkdir()
    subprocess.run(["git", "init", "-q", str(target)], check=True)
    plan = installer.install(target, "lvlaksim1/example", dry_run=True)
    check(len(plan) == 6 and not (target / "quality").exists(), "dry run changed files")
    writes = installer.install(target, "lvlaksim1/example")
    check(len(writes) == 6, "installation count")
    check(all(x.startswith("UNCHANGED") for x in installer.install(target, "lvlaksim1/example")), "idempotency")
    architecture = target / "scripts" / "architecture_explorer.py"
    check(architecture.exists(), "architecture analyzer not installed")
    (target / "src" / "A").mkdir(parents=True)
    (target / "src" / "B").mkdir(parents=True)
    (target / "src" / "A" / "A.csproj").write_text(
        '<Project><ItemGroup><ProjectReference Include="../B/B.csproj" /></ItemGroup></Project>',
        encoding="utf-8")
    (target / "src" / "B" / "B.csproj").write_text('<Project />', encoding="utf-8")
    analyzer_result = subprocess.run([sys.executable, str(architecture), "--check"],
                                     cwd=target, capture_output=True, text=True)
    check(analyzer_result.returncode == 0, "architecture graph failed")
    graph = json.loads((target / "quality" / "reports" / "architecture.json").read_text(encoding="utf-8"))
    check(graph["project_count"] == 2 and graph["reference_count"] == 1, "graph edges incorrect")
    check((target / "quality" / "reports" / "architecture.html").exists(), "HTML missing")
    # Architecture regression: cycles and missing project references must fail.
    a = target / "src" / "A" / "A.csproj"
    b = target / "src" / "B" / "B.csproj"
    b.write_text('<Project><ItemGroup><ProjectReference Include="../A/A.csproj" /></ItemGroup></Project>',
                 encoding="utf-8")
    broken = subprocess.run([sys.executable, str(architecture), "--check"],
                            cwd=target, capture_output=True, text=True)
    check(broken.returncode == 1 and "CYCLES=" in broken.stdout, "cycle not detected")
    b.write_text('<Project />', encoding="utf-8")
    a.write_text('<Project><ItemGroup><ProjectReference Include="../MISSING/M.csproj" /></ItemGroup></Project>',
                 encoding="utf-8")
    broken = subprocess.run([sys.executable, str(architecture), "--check"],
                            cwd=target, capture_output=True, text=True)
    check(broken.returncode == 1 and "UNRESOLVED=1" in broken.stdout, "missing project not detected")
    a.write_text('<Project><ItemGroup><ProjectReference Include="../B/B.csproj" /></ItemGroup></Project>',
                 encoding="utf-8")
    subprocess.run(["git", "-C", str(target), "add", "src"], check=True)
    sanity = target / "scripts" / "quality_source_sanity.py"
    check(sanity.exists(), "source sanity script absent")
    sanity_result = subprocess.run([sys.executable,str(sanity)], cwd=target, capture_output=True, text=True)
    check(sanity_result.returncode == 0 and "SOURCE_SANITY_PASS" in sanity_result.stdout, "syntax check failed")
    runner = target / "scripts" / "quality_runner.py"
    p = subprocess.run([sys.executable, str(runner), "--profile", "quick"],
                       cwd=target, capture_output=True, text=True)
    check(p.returncode == 1 and "NOT_CONFIGURED" in p.stdout, "empty suite false success")
    config_path = target / "quality" / "standard.json"
    data = json.loads(config_path.read_text(encoding="utf-8"))
    data["quick"] = [{"id": "selftest", "kind": "unit",
                      "command": ["python", "-c", "print('PASS')"], "timeout_sec": 8}]
    config_path.write_text(json.dumps(data), encoding="utf-8")
    p = subprocess.run([sys.executable, str(runner), "--profile", "full"],
                       cwd=target, capture_output=True, text=True)
    check(p.returncode == 0 and "OFFLINE_GATE=PASS" in p.stdout, "configured suite failed")
    reports = list((target / "quality" / "reports").glob("quality-full-*.json"))
    check(len(reports) == 1, "missing report")
    report = json.loads(reports[0].read_text(encoding="utf-8"))
    check(report["live_e2e"] == "NOT_TESTED" and not report["release_authorized"],
          "incorrect live acceptance claim")
    data["quick"] = [{"id": "failure", "kind": "unit",
                      "command": ["python", "-c", "import sys;sys.exit(3)"], "timeout_sec": 8},
                     {"id": "skip", "kind": "unit",
                      "command": ["python", "-c", "print('should not execute')"], "timeout_sec": 8}]
    config_path.write_text(json.dumps(data), encoding="utf-8")
    p = subprocess.run([sys.executable, str(runner)], cwd=target,
                       capture_output=True, text=True)
    check(p.returncode == 1 and "NOT_RUN" in p.stdout, "fail fast incorrectly passed")
    try:
        installer.install(target, "lvlaksim1/example")
    except ValueError:
        pass
    else:
        raise AssertionError("Existing differing config overwritten")
    check(not (target / "quality" / "reports" / ".gitignore").exists(), "unexpected report mutation")
print("ENGINEERING_QUALITY_FACTORY_TESTS_PASS")
