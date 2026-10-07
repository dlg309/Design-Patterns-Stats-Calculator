import subprocess
import sys
from pathlib import Path


def test_module_runs_interactive_session():
    project_root = Path(__file__).resolve().parents[1]

    completed = subprocess.run(
        [sys.executable, "-m", "calculator"],
        cwd=project_root,
        input=(
            "add 2 3\n"
            "divide 1 0\n"
            "multiply 4 3\n"
            "history\n"
            "clear\n"
            "history\n"
            "exit\n"
        ),
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )

    output = completed.stdout

    assert "Result: 5.0000" in output
    assert "Error: float division by zero" in output
    assert "Result: 12.0000" in output
    assert "add 2.0 3.0 = 5.0000" in output
    assert "multiply 4.0 3.0 = 12.0000" in output
    assert "divide 1.0 0.0 =" not in output
    assert "History cleared." in output
    assert "History is empty." in output
    assert "Goodbye!" in output
    assert completed.stderr == ""
