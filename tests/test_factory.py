import pytest

from calculator.calculation import Calculation
from calculator.factory import CalculationFactory


@pytest.mark.parametrize(
    "name, a, b, expected",
    [
        ("add", 2, 3, 5),
        ("subtract", 8, 3, 5),
        ("multiply", 4, 3, 12),
        ("divide", 9, 2, 4.5),
        ("absolute_difference", 2, 8, 6),
    ],
)
def test_factory_creates_calculations(name, a, b, expected):
    calculation = CalculationFactory.create(name, a, b)

    assert isinstance(calculation, Calculation)
    assert calculation.get_result() == pytest.approx(expected)


def test_factory_normalizes_operation_name():
    calculation = CalculationFactory.create(" ADD ", "2", "3")

    assert calculation.get_result() == 5.0


def test_factory_rejects_unknown_operation():
    with pytest.raises(ValueError, match="Unknown operation: missing"):
        CalculationFactory.create("missing", 2, 3)


def test_factory_preserves_operand_validation_error():
    with pytest.raises(ValueError, match="must be a number"):
        CalculationFactory.create("add", "hello", 3)


def test_factory_defers_division_until_execution():
    calculation = CalculationFactory.create("divide", 5, 0)

    with pytest.raises(ZeroDivisionError):
        calculation.get_result()


def test_factory_does_not_execute_operation(monkeypatch):
    calls = []

    def tracked_add(a, b):
        calls.append((a, b))
        return a + b

    monkeypatch.setitem(
        CalculationFactory.operations, "add", tracked_add
    )

    calculation = CalculationFactory.create("add", 2, 3)

    assert calls == []

    assert calculation.get_result() == 5.0
    assert calls == [(2.0, 3.0)]


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 3, 1),
        (12, 4, 0),
        (7.5, 2, 1.5),
    ],
)
def test_factory_supports_modulo(a, b, expected):
    calculation = CalculationFactory.create("modulo", a, b)

    assert calculation.get_result() == pytest.approx(expected)


def test_factory_normalizes_modulo_name():
    calculation = CalculationFactory.create(" MODULO ", 10, 3)

    assert calculation.get_result() == 1.0


def test_modulo_by_zero_fails_during_execution():
    calculation = CalculationFactory.create("modulo", 10, 0)

    with pytest.raises(ZeroDivisionError):
        calculation.get_result()
