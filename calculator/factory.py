"""Select an operation and validate operands and named settings."""

from calculator.calculation import Calculation
from calculator.operations import Operations
from calculator.validation import numeric_values


class CalculationFactory:
    operations = {
        "mean": Operations.mean,
        "stddev": Operations.stddev,
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide,
        "absolute_difference": Operations.absolute_difference,
        "modulo": Operations.modulo,
        "square": Operations.square,
        "sqrt": Operations.sqrt,
        "sum": Operations.sum,
        "power": Operations.power,
        "scale": Operations.scale,

    }

    arities = {
        "add": 2,
        "subtract": 2,
        "multiply": 2,
        "divide": 2,
        "absolute_difference": 2,
        "modulo": 2,
        "square": 1,
        "sqrt": 1,
        "power": 1,
        "scale": 1,
    }

    allowed_options = {
        "stddev": {"ddof"},
        "power": {"exponent"},
        "scale": {"factor"},
    }

    @staticmethod
    def create(name, *values, **options):
        name = name.strip().lower()

        try:
            operation = CalculationFactory.operations[name]
        except KeyError:
            raise ValueError(f"Unknown operation: {name}") from None

        allowed = CalculationFactory.allowed_options.get(name, set())
        converted_options = {}

        for key, value in options.items():
            if key not in allowed:
                raise ValueError(f"Unsupported option for {name}: {key}")

            converted_options[key] = numeric_values([value])[0]

        expected = CalculationFactory.arities.get(name)
        if expected is not None and len(values) != expected:
            raise ValueError(
                f"{name} requires exactly {expected} operand(s)."
            )

        return Calculation(values, operation, **converted_options)
