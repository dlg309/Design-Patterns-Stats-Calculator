import pytest

from calculator.operations import Operations


@pytest.mark.parametrize(
    "operation, a, b, expected",
    [
        (Operations.add, 2, 3, 5),
        (Operations.subtract, 8, 3, 5),
        (Operations.multiply, 4, 3, 12),
        (Operations.divide, 9, 2, 4.5),
        (Operations.add, -2, 3, 1),
        (Operations.subtract, 2, 5, -3),
        (Operations.multiply, 4, 0, 0),
    ],
)
def test_operations(operation, a, b, expected):
    assert operation(a, b) == pytest.approx(expected)


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        Operations.divide(5, 0)


@pytest.mark.parametrize(
    "value, expected",
    [
        (4, 16),
        (-3, 9),
        (0, 0),
    ],
)
def test_square(value, expected):
    assert Operations.square(value) == pytest.approx(expected)


def test_square_root():
    assert Operations.sqrt(9) == pytest.approx(3)


def test_square_root_rejects_negative_value():
    with pytest.raises(ValueError):
        Operations.sqrt(-1)


@pytest.mark.parametrize(
    "values, expected",
    [
        ((2, 3, 4), 9),
        ((5,), 5),
        ((-2, 2), 0),
    ],
)
def test_sum(values, expected):
    assert Operations.sum(*values) == pytest.approx(expected)


def test_sum_rejects_empty_input():
    with pytest.raises(ValueError, match="at least one value"):
        Operations.sum()
