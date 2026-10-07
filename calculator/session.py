"""Store successful calculations and separately recorded failures."""

from calculator.history import History


class CalculatorSession:
    def __init__(self):
        self._history = History()
        self._errors = []

    def calculate(self, calculation):
        result = calculation.get_result()
        self._history.add(calculation, result)
        return result

    def get_history(self):
        return self._history.get_history()

    def record_failure(self, error):
        self._errors.append(str(error))

    def get_errors(self):
        return self._errors.copy()

    def clear(self):
        self._history.clear()
        self._errors.clear()
