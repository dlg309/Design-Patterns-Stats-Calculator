"""Run the Part 3 flexible-input demonstration."""

from calculator.factory import CalculationFactory
from calculator.history import History


def main():
    history = History()
    calculations = [
        CalculationFactory.create("add", 2, 3),
        CalculationFactory.create("power", 3, exponent=4),
    ]

    for calculation in calculations:
        result = calculation.get_result()
        history.add(calculation, result)
        print(result)


if __name__ == "__main__":
    main()
