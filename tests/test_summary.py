import pytest

from calculator.cli import prepare_command, run
from calculator.commands import SummaryCommand
from calculator.sequence import execute_requests
from calculator.session import CalculatorSession


def test_summary_starts_at_zero():
    session = CalculatorSession()

    assert SummaryCommand(session).execute() == "Successful: 0; Failed: 0"


def test_summary_counts_preparation_and_execution_failures_once():
    session = CalculatorSession()

    execute_requests(session, [
        ("add", [2, 3], {}),
        ("missing", [2, 3], {}),
        ("divide", [1, 0], {}),
        ("square", [4], {}),
    ])

    assert SummaryCommand(session).execute() == "Successful: 2; Failed: 2"

    copied_errors = session.get_errors()
    copied_errors.clear()

    assert len(session.get_errors()) == 2


def test_clear_resets_successes_and_failures():
    session = CalculatorSession()
    execute_requests(session, [
        ("add", [2, 3], {}),
        ("divide", [1, 0], {}),
    ])

    prepare_command("clear", session).execute()

    assert SummaryCommand(session).execute() == "Successful: 0; Failed: 0"
    assert session.get_history() == []
    assert session.get_errors() == []


def test_summary_rejects_extra_arguments():
    with pytest.raises(ValueError, match="summary does not accept arguments"):
        prepare_command("summary extra", CalculatorSession())


def test_interactive_summary_and_clear(monkeypatch, capsys):
    responses = iter([
        "missing",
        "divide 1 0",
        "add 2 3",
        "summary",
        "clear",
        "summary",
        "exit",
    ])
    monkeypatch.setattr("builtins.input", lambda prompt: next(responses))

    run()

    output = capsys.readouterr().out
    assert "Successful: 1; Failed: 2" in output
    assert "Successful: 0; Failed: 0" in output
