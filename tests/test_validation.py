import pytest

from calculator.validation import numeric_values


def test_converts_numbers_and_numeric_strings():
    assert numeric_values([2, "3.5", -4]) == (2.0, 3.5, -4.0)


@pytest.mark.parametrize("value", ["hello", "", None])
def test_rejects_invalid_values(value):
    with pytest.raises(ValueError, match="must be a number"):
        numeric_values([value])


@pytest.mark.parametrize("value", [float("inf"), float("-inf"), float("nan")])
def test_rejects_nonfinite_values(value):
    with pytest.raises(ValueError, match="must be finite"):
        numeric_values([value])
