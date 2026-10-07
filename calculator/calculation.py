"""Store validated operands and execute an operation on request."""

from math import isfinite

from calculator.validation import numeric_values


class Calculation:
    def __init__(self, a, b, operation):
        numbers = numeric_values([a, b])
        self.a = numbers[0]
        self.b = numbers[1]
        self.operation = operation

    def get_result(self):
        result = float(self.operation(self.a, self.b))

        if not isfinite(result):
            raise ValueError("Result is outside the supported range.")

        return result
