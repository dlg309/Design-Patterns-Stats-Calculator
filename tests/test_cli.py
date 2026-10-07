import pytest

from calculator.cli import prepare_command
from calculator.commands import (
    ClearHistoryCommand,
    HelpCommand,
    HistoryCommand,
)
from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession


@pytest.mark.parametrize(
    "line, expected_type",
    [
        ("help", HelpCommand),
        ("history", HistoryCommand),
        ("clear", ClearHistoryCommand),
        ("  HELP  ", HelpCommand),
    ],
)
def test_prepare_application_command(line, expected_type):
    session = CalculatorSession()

    command = prepare_command(line, session)

    assert isinstance(command, expected_type)


@pytest.mark.parametrize("line", ["", "   "])
def test_prepare_rejects_empty_input(line):
    with pytest.raises(ValueError, match="Enter a command"):
        prepare_command(line, CalculatorSession())


@pytest.mark.parametrize("line", ["help extra", "history extra", "clear extra"])
def test_application_commands_reject_arguments(line):
    with pytest.raises(ValueError, match="does not accept arguments"):
        prepare_command(line, CalculatorSession())


def test_prepare_rejects_unknown_command():
    with pytest.raises(ValueError, match="Unknown command: missing"):
        prepare_command("missing", CalculatorSession())


def test_preparing_clear_does_not_clear_until_execution():
    session = CalculatorSession()
    calculation = CalculationFactory.create("add", 2, 3)
    session.calculate(calculation)

    command = prepare_command("clear", session)

    assert session.get_history() == [(calculation, 5.0)]

    assert command.execute() == "History cleared."
    assert session.get_history() == []


@pytest.mark.parametrize(
    "line, expected",
    [
        ("add 2 3", "Result: 5.0000"),
        ("power 3 exponent=4", "Result: 81.0000"),
        ("sum 10 20 30", "Result: 60.0000"),
        ("scale 12 factor=3", "Result: 4.0000"),
        ("  ADD   2   3  ", "Result: 5.0000"),
    ],
)
def test_prepare_math_request(line, expected):
    session = CalculatorSession()

    command = prepare_command(line, session)

    assert session.get_history() == []
    assert command.execute() == expected
    assert len(session.get_history()) == 1


def test_prepare_rejects_duplicate_options():
    with pytest.raises(ValueError, match="Duplicate option: exponent"):
        prepare_command(
            "power 3 exponent=2 exponent=4",
            CalculatorSession(),
        )


@pytest.mark.parametrize("line", ["power 3 exponent=", "power 3 =4"])
def test_prepare_rejects_malformed_options(line):
    with pytest.raises(ValueError, match="Options must use key=value"):
        prepare_command(line, CalculatorSession())


def test_prepare_rejects_unsupported_option():
    with pytest.raises(ValueError, match="Unsupported option"):
        prepare_command("add 2 3 exponent=4", CalculatorSession())


def test_prepare_rejects_invalid_numeric_input():
    with pytest.raises(ValueError, match="must be a number"):
        prepare_command("add hello 3", CalculatorSession())


def test_prepare_rejects_wrong_operand_count():
    with pytest.raises(ValueError, match="requires exactly"):
        prepare_command("add 2", CalculatorSession())


def test_prepared_division_fails_only_when_executed():
    session = CalculatorSession()

    command = prepare_command("divide 1 0", session)

    with pytest.raises(ZeroDivisionError):
        command.execute()

    assert session.get_history() == []


def test_run_recovers_from_invalid_input(monkeypatch, capsys):
    from calculator.cli import run

    responses = iter(["add hello 3", "add 2 3", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(responses))

    run()

    output = capsys.readouterr().out
    assert "Error: Each value must be a number." in output
    assert "Result: 5.0000" in output
    assert "Goodbye!" in output


def test_run_ignores_blank_lines_and_accepts_uppercase_exit(
    monkeypatch, capsys
):
    from calculator.cli import run

    responses = iter(["   ", "EXIT"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(responses))

    run()

    output = capsys.readouterr().out
    assert "Error:" not in output
    assert "Goodbye!" in output


@pytest.mark.parametrize("exception_type", [EOFError, KeyboardInterrupt])
def test_run_exits_cleanly_on_interruption(
    monkeypatch, capsys, exception_type
):
    from calculator.cli import run

    def interrupted_input(prompt):
        raise exception_type()

    monkeypatch.setattr("builtins.input", interrupted_input)

    run()

    assert "Goodbye!" in capsys.readouterr().out


def test_count_starts_at_zero():
    session = CalculatorSession()

    assert (
        prepare_command("count", session).execute()
        == "Calculations in history: 0"
    )


def test_count_includes_only_successful_calculations():
    session = CalculatorSession()
    prepare_command("add 2 3", session).execute()

    with pytest.raises(ZeroDivisionError):
        prepare_command("divide 1 0", session).execute()

    prepare_command("multiply 4 3", session).execute()

    assert (
        prepare_command("count", session).execute()
        == "Calculations in history: 2"
    )


def test_count_returns_zero_after_clear():
    session = CalculatorSession()
    prepare_command("add 2 3", session).execute()
    prepare_command("clear", session).execute()

    assert (
        prepare_command("count", session).execute()
        == "Calculations in history: 0"
    )


def test_count_rejects_extra_arguments():
    with pytest.raises(ValueError, match="count does not accept arguments"):
        prepare_command("count extra", CalculatorSession())


def test_help_lists_count():
    assert "count" in prepare_command("help", CalculatorSession()).execute()
