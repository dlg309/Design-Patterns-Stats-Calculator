"""Arithmetic operations that do not require instance state."""

class Operations:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        return a / b
    @staticmethod
    def absolute_difference(a, b):
        return abs(a - b)

    @staticmethod
    def modulo(a, b):
        return a % b

    @staticmethod
    def square(value):
        return value * value

    @staticmethod
    def sqrt(value):
        from math import sqrt

        return sqrt(value)

    @staticmethod
    def sum(*values):
        if not values:
            raise ValueError("Sum requires at least one value.")

        return sum(values)

    @staticmethod
    def power(value, *, exponent=2):
        from math import pow

        return pow(value, exponent)

    @staticmethod
    def scale(value, *, factor=1):
        return value / factor

    @staticmethod
    def mean(*values):
        from calculator.statistics import mean

        return mean(values)

    @staticmethod
    def stddev(*values, ddof=1):
        from calculator.statistics import standard_deviation

        return standard_deviation(values, ddof=ddof)
