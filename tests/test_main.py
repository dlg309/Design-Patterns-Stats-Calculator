import subprocess
import sys
from pathlib import Path


def test_module_prints_demonstration_result():
    project_root = Path(__file__).resolve().parents[1]

    completed = subprocess.run(
        [sys.executable, "-m", "calculator"],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=True,
    )

    assert completed.stdout.strip() == "5.0"
    assert completed.stderr == ""
