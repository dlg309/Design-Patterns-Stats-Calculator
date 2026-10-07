import pytest

from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession


def test_session_starts_with_empty_history():
    session = CalculatorSession()

    assert session.get_history() == []


def test_session_returns_and_records_success():
    session = CalculatorSession()
    calculation = CalculationFactory.create("add", 2, 3)

    result = session.calculate(calculation)

    assert result == 5.0
    assert session.get_history() == [(calculation, 5.0)]


def test_failed_calculation_preserves_previous_history():
    session = CalculatorSession()
    successful = CalculationFactory.create("add", 2, 3)
    session.calculate(successful)

    failing = CalculationFactory.create("divide", 1, 0)

    with pytest.raises(ZeroDivisionError):
        session.calculate(failing)

    assert session.get_history() == [(successful, 5.0)]


def test_session_can_calculate_after_failure():
    session = CalculatorSession()
    failing = CalculationFactory.create("divide", 1, 0)

    with pytest.raises(ZeroDivisionError):
        session.calculate(failing)

    successful = CalculationFactory.create("multiply", 4, 3)

    assert session.calculate(successful) == 12.0
    assert session.get_history() == [(successful, 12.0)]


def test_session_clear_removes_history():
    session = CalculatorSession()
    session.calculate(CalculationFactory.create("add", 2, 3))

    session.clear()

    assert session.get_history() == []


def test_returned_history_list_cannot_erase_saved_entries():
    session = CalculatorSession()
    calculation = CalculationFactory.create("add", 2, 3)
    session.calculate(calculation)

    copied_history = session.get_history()
    copied_history.clear()

    assert session.get_history() == [(calculation, 5.0)]


def test_sessions_have_independent_histories():
    first = CalculatorSession()
    second = CalculatorSession()

    first.calculate(CalculationFactory.create("add", 2, 3))

    assert len(first.get_history()) == 1
    assert second.get_history() == []
