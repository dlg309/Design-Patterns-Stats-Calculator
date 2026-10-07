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
