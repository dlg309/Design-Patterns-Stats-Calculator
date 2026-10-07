"""Run the Part 2 factory demonstration."""

from calculator.factory import CalculationFactory
from calculator.history import History


def main():
    history = History()
    calculation = CalculationFactory.create("add", 2, 3)

    result = calculation.get_result()
    history.add(calculation, result)

    print(result)


if __name__ == "__main__":
    main()
