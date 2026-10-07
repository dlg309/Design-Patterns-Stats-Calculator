"""Convert inputs into finite numeric values."""

from math import isfinite


def numeric_values(values):
    numbers = []

    for value in values:
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ValueError("Each value must be a number.") from None

        if not isfinite(number):
            raise ValueError("Each value must be finite.")

        numbers.append(number)

    return tuple(numbers)
