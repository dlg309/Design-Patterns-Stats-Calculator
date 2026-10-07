import pytest

from calculator.calculation import Calculation
from calculator.operations import Operations


def test_add_calculation():
    calculation = Calculation([2, 3], Operations.add)
    assert calculation.get_result() == 5


def test_subtract_calculation():
    calculation = Calculation([8, 3], Operations.subtract)
    assert calculation.get_result() == 5


def test_operation_runs_only_when_result_is_requested():
    calls = []

    def spy_operation(a, b):
        calls.append((a, b))
        return a + b

    calculation = Calculation([2, 3], spy_operation)

    assert calls == []

    result = calculation.get_result()

    assert result == 5
    assert calls == [(2, 3)]


def test_division_by_zero_fails_during_execution():
    calculation = Calculation([5, 0], Operations.divide)

    with pytest.raises(ZeroDivisionError):
        calculation.get_result()


def test_calculation_accepts_numeric_strings():
    calculation = Calculation(["2", "3.5"], Operations.add)
    assert calculation.get_result() == pytest.approx(5.5)


def test_calculation_rejects_invalid_operand():
    with pytest.raises(ValueError, match="must be a number"):
        Calculation(["hello", 3], Operations.add)


def test_calculation_rejects_infinite_operand():
    with pytest.raises(ValueError, match="must be finite"):
        Calculation([float("inf"), 3], Operations.add)


def test_calculation_rejects_nonfinite_result():
    calculation = Calculation([1e308, 1e308], Operations.multiply)

    with pytest.raises(ValueError, match="outside the supported range"):
        calculation.get_result()


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 8, 6),
        (8, 2, 6),
        (-2, -8, 6),
        (4, 4, 0),
    ],
)
def test_absolute_difference(a, b, expected):
    calculation = Calculation([a, b], Operations.absolute_difference)
    assert calculation.get_result() == pytest.approx(expected)


def test_calculation_snapshots_input_values():
    values = [2, 3]
    calculation = Calculation(values, Operations.add)

    values[0] = 100
    values.append(4)

    assert calculation.values == (2.0, 3.0)
    assert calculation.get_result() == 5.0
