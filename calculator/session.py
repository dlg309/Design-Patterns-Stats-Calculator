"""Execute calculations and record successful results."""

from calculator.history import History


class CalculatorSession:
    def __init__(self):
        self._history = History()

    def calculate(self, calculation):
        result = calculation.get_result()
        self._history.add(calculation, result)
        return result

    def get_history(self):
        return self._history.get_history()

    def clear(self):
        self._history.clear()
