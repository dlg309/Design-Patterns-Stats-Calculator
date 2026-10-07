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
