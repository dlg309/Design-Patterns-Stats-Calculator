import pytest

from calculator.factory import CalculationFactory
from calculator.sequence import execute_sequence
from calculator.session import CalculatorSession


def test_sequence_continues_after_failure():
    session = CalculatorSession()
    first = CalculationFactory.create("add", 2, 3)
    failing = CalculationFactory.create("divide", 1, 0)
    last = CalculationFactory.create("square", 3)

    results, errors = execute_sequence(
        session, [first, failing, last]
    )

    assert results == [5.0, 9.0]
    assert len(errors) == 1
    assert "division by zero" in errors[0]
    assert session.get_history() == [(first, 5.0), (last, 9.0)]


def test_empty_sequence_preserves_existing_history():
    session = CalculatorSession()
    previous = CalculationFactory.create("add", 10, 20)
    session.calculate(previous)

    results, errors = execute_sequence(session, [])

    assert results == []
    assert errors == []
    assert session.get_history() == [(previous, 30.0)]


def test_sequence_records_multiple_failures():
    session = CalculatorSession()
    calculations = [
        CalculationFactory.create("divide", 1, 0),
        CalculationFactory.create("sqrt", -1),
    ]

    results, errors = execute_sequence(session, calculations)

    assert results == []
    assert len(errors) == 2
    assert session.get_history() == []


def test_sequence_handles_overflow_and_continues():
    session = CalculatorSession()
    overflowing = CalculationFactory.create("power", 10, exponent=1000)
    successful = CalculationFactory.create("mean", 2, 4, 6)

    results, errors = execute_sequence(
        session, [overflowing, successful]
    )

    assert results == [4.0]
    assert len(errors) == 1
    assert session.get_history() == [(successful, 4.0)]


def test_sequence_does_not_hide_unexpected_programming_errors():
    from calculator.calculation import Calculation

    def broken_operation(value):
        raise RuntimeError("Unexpected implementation failure.")

    calculation = Calculation([2], broken_operation)
    session = CalculatorSession()

    with pytest.raises(RuntimeError, match="Unexpected implementation"):
        execute_sequence(session, [calculation])

    assert session.get_history() == []


def test_requests_continue_after_preparation_and_execution_failures():
    from calculator.sequence import execute_requests

    session = CalculatorSession()
    requests = [
        ("add", [2, 3], {}),
        ("missing", [2, 3], {}),
        ("divide", [1, 0], {}),
        ("power", [3], {"exponent": 4}),
    ]

    results, errors = execute_requests(session, requests)

    assert results == [5.0, 81.0]
    assert len(errors) == 2
    assert "Unknown operation: missing" in errors[0]
    assert "division by zero" in errors[1]

    history = session.get_history()
    assert [result for calculation, result in history] == [5.0, 81.0]
    assert [
        calculation.operation.__name__
        for calculation, result in history
    ] == ["add", "power"]


@pytest.mark.parametrize(
    "bad_request",
    [
        ("add", [2], {}),
        ("add", ["hello", 3], {}),
        ("power", [3], {"unknown": 4}),
        ("stddev", [2, 4, 6], {"ddof": 2}),
    ],
)
def test_invalid_request_does_not_prevent_later_success(bad_request):
    from calculator.sequence import execute_requests

    session = CalculatorSession()

    results, errors = execute_requests(
        session,
        [bad_request, ("square", [4], {})],
    )

    assert results == [16.0]
    assert len(errors) == 1
    assert len(session.get_history()) == 1


def test_empty_requests_preserve_existing_history():
    from calculator.sequence import execute_requests

    session = CalculatorSession()
    previous = CalculationFactory.create("add", 2, 3)
    session.calculate(previous)

    results, errors = execute_requests(session, [])

    assert results == []
    assert errors == []
    assert session.get_history() == [(previous, 5.0)]
