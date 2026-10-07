"""Statistical operations with explicit numeric validation."""

from math import isfinite

import pandas as pd

from calculator.validation import numeric_values


def mean(values):
    numbers = numeric_values(values)

    if not numbers:
        raise ValueError("Enter at least one value.")

    result = float(pd.Series(numbers, dtype=float).mean())

    if not isfinite(result):
        raise ValueError("Result is outside the supported range.")

    return result


def standard_deviation(values, *, ddof=1):
    if ddof not in (0, 1):
        raise ValueError("ddof must be 0 (population) or 1 (sample).")

    numbers = numeric_values(values)

    if len(numbers) < 2:
        raise ValueError("Enter at least two values.")

    result = float(pd.Series(numbers, dtype=float).std(ddof=ddof))

    if not isfinite(result):
        raise ValueError("Result is outside the supported range.")

    return result
