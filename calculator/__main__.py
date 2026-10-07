"""Run the Part 1 calculation demonstration."""

from calculator.calculation import Calculation
from calculator.history import History
from calculator.operations import Operations


def main():
    history = History()
    calculation = Calculation(2, 3, Operations.add)

    result = calculation.get_result()
    history.add(calculation, result)

    print(result)


if __name__ == "__main__":
    main()
