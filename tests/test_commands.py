import pytest

from calculator.commands import (
    CalculateCommand,
    ClearHistoryCommand,
    Command,
    HelpCommand,
    HistoryCommand,
)
from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession


def test_incomplete_command_cannot_be_instantiated():
    class IncompleteCommand(Command):
        pass

    with pytest.raises(TypeError):
        IncompleteCommand()


def test_calculate_command_returns_text_and_records_result(capsys):
    session = CalculatorSession()
    calculation = CalculationFactory.create("add", 2, 3)
    command = CalculateCommand(session, calculation)

    assert command.execute() == "Result: 5.0000"
    assert session.get_history() == [(calculation, 5.0)]
    assert capsys.readouterr().out == ""


def test_command_construction_does_not_execute_calculation():
    session = CalculatorSession()
    calculation = CalculationFactory.create("divide", 1, 0)

    command = CalculateCommand(session, calculation)

    assert session.get_history() == []

    with pytest.raises(ZeroDivisionError):
        command.execute()

    assert session.get_history() == []


def test_history_command_handles_empty_history():
    session = CalculatorSession()

    assert HistoryCommand(session).execute() == "History is empty."


def test_history_command_displays_saved_result_without_recalculation():
    session = CalculatorSession()
    calculation = CalculationFactory.create("add", 2, 3)
    session.calculate(calculation)

    def add(a, b):
        raise AssertionError("History must not rerun the operation.")

    calculation.operation = add

    assert HistoryCommand(session).execute() == "add 2.0 3.0 = 5.0000"


def test_history_command_displays_named_options():
    session = CalculatorSession()
    calculation = CalculationFactory.create("power", 3, exponent=4)
    session.calculate(calculation)

    assert (
        HistoryCommand(session).execute()
        == "power 3.0 exponent=4.0 = 81.0000"
    )


def test_clear_command_removes_history():
    session = CalculatorSession()
    session.calculate(CalculationFactory.create("add", 2, 3))

    assert ClearHistoryCommand(session).execute() == "History cleared."
    assert session.get_history() == []


def test_help_command_includes_supported_syntax():
    text = HelpCommand().execute()

    for expected in ("power", "exponent=N", "scale", "history", "exit"):
        assert expected in text
