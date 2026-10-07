"""Select an operation and construct a calculation without executing it."""

from calculator.calculation import Calculation
from calculator.operations import Operations


class CalculationFactory:
    operations = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide,
        "absolute_difference": Operations.absolute_difference,
        "modulo": Operations.modulo,
    }

    @staticmethod
    def create(name, a, b):
        name = name.strip().lower()

        try:
            operation = CalculationFactory.operations[name]
        except KeyError:
            raise ValueError(f"Unknown operation: {name}") from None

        return Calculation(a, b, operation)
