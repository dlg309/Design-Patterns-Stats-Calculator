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


@pytest.mark.parametrize(
    "line, expected",
    [
        ("mean 10 20 30 40 50", "Result: 30.0000"),
        ("stddev 10 20 30 40 50", "Result: 15.8114"),
        ("stddev 2 4 6 ddof=0", "Result: 1.6330"),
        ("stddev 2 4 6 ddof=1", "Result: 2.0000"),
        ("mean 7", "Result: 7.0000"),
    ],
)
def test_statistics_requests(line, expected):
    session = CalculatorSession()
    command = prepare_command(line, session)

    assert session.get_history() == []
    assert command.execute() == expected
    assert len(session.get_history()) == 1


@pytest.mark.parametrize(
    "line",
    [
        "mean",
        "stddev 7",
        "stddev 7 ddof=0",
        "stddev 2 4 6 ddof=2",
    ],
)
def test_statistics_execution_failure_does_not_enter_history(line):
    session = CalculatorSession()
    command = prepare_command(line, session)

    with pytest.raises(ValueError):
        command.execute()

    assert session.get_history() == []


def test_mean_rejects_ddof_option():
    with pytest.raises(ValueError, match="Unsupported option"):
        prepare_command("mean 2 4 6 ddof=0", CalculatorSession())


def test_stddev_rejects_nonnumeric_ddof():
    with pytest.raises(ValueError, match="must be a number"):
        prepare_command("stddev 2 4 6 ddof=hello", CalculatorSession())


@pytest.mark.parametrize(
    "operation, options, expected",
    [
        ("mean", "", "Result: 4.0000"),
        ("stddev", "", "Result: 2.0000"),
        ("stddev", "ddof=0", "Result: 1.6330"),
    ],
)
def test_csv_request(tmp_path, operation, options, expected):
    path = tmp_path / "values.csv"
    path.write_text("value\n2\n4\n6\n")
    session = CalculatorSession()

    command = prepare_command(
        f"csv {operation} {path} {options}", session
    )

    assert session.get_history() == []
    assert command.execute() == expected
    assert len(session.get_history()) == 1


@pytest.mark.parametrize("line", ["csv", "csv mean"])
def test_csv_requires_operation_and_path(line):
    with pytest.raises(ValueError, match="Usage: csv"):
        prepare_command(line, CalculatorSession())


def test_csv_rejects_unsupported_operation():
    with pytest.raises(ValueError, match="supports mean and stddev only"):
        prepare_command("csv add values.csv", CalculatorSession())


def test_csv_rejects_extra_positional_values():
    with pytest.raises(ValueError, match="settings must use key=value"):
        prepare_command("csv mean values.csv 42", CalculatorSession())


def test_csv_rejects_duplicate_options():
    with pytest.raises(ValueError, match="Duplicate option"):
        prepare_command(
            "csv stddev values.csv ddof=0 ddof=1",
            CalculatorSession(),
        )


@pytest.mark.parametrize("file_kind", ["missing", "empty", "malformed"])
def test_run_recovers_from_csv_file_errors(
    tmp_path, monkeypatch, capsys, file_kind
):
    from calculator.cli import run

    path = tmp_path / "values.csv"

    if file_kind == "empty":
        path.write_text("")
    elif file_kind == "malformed":
        path.write_text('value\n"unterminated\n')

    responses = iter([
        f"csv mean {path}",
        "add 2 3",
        "count",
        "exit",
    ])
    monkeypatch.setattr("builtins.input", lambda prompt: next(responses))

    run()

    output = capsys.readouterr().out
    assert "Error:" in output
    assert "Result: 5.0000" in output
    assert "Calculations in history: 1" in output
    assert "Goodbye!" in output


def test_csv_mean_uses_selected_column(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text("value,score\n100,2\n200,4\n300,6\n")
    session = CalculatorSession()

    command = prepare_command(
        f"csv mean {path} column=score", session
    )

    assert command.execute() == "Result: 4.0000"


def test_csv_selected_column_supports_math_options(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text("score\n2\n4\n6\n")
    session = CalculatorSession()

    command = prepare_command(
        f"csv stddev {path} column=score ddof=0", session
    )

    assert command.execute() == "Result: 1.6330"


def test_csv_selected_column_preserves_numeric_validation(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text("score\n2\nhello\n6\n")
    session = CalculatorSession()

    with pytest.raises(ValueError, match="must be a number"):
        prepare_command(f"csv mean {path} column=score", session)

    assert session.get_history() == []
