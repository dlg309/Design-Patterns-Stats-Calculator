"""Application actions with a shared execution contract."""

from abc import ABC, abstractmethod


HELP = (
    "Commands: add/subtract/multiply/divide/modulo/absolute_difference A B; "
    "square/sqrt VALUE; power VALUE exponent=N; scale VALUE factor=N; "
    "csv mean|stddev PATH [column=NAME] [ddof=0|1]; sum VALUES; mean VALUES; stddev VALUES ddof=0|1; history; clear; count; help; exit"
)


class Command(ABC):
    @abstractmethod
    def execute(self) -> str:
        """Perform an action and return display text."""


class CalculateCommand(Command):
    def __init__(self, session, calculation):
        self.session = session
        self.calculation = calculation

    def execute(self) -> str:
        result = self.session.calculate(self.calculation)
        return f"Result: {result:.4f}"


class HistoryCommand(Command):
    def __init__(self, session):
        self.session = session

    def execute(self) -> str:
        lines = []

        for calculation, result in self.session.get_history():
            values = " ".join(str(value) for value in calculation.values)
            options = " ".join(
                f"{key}={value}"
                for key, value in calculation.options.items()
            )
            parts = [calculation.operation.__name__, values, options]
            request = " ".join(part for part in parts if part)
            lines.append(f"{request} = {result:.4f}")

        return "\n".join(lines) or "History is empty."


class ClearHistoryCommand(Command):
    def __init__(self, session):
        self.session = session

    def execute(self) -> str:
        self.session.clear()
        return "History cleared."


class HelpCommand(Command):
    def execute(self) -> str:
        return HELP


class CountCommand(Command):
    def __init__(self, session):
        self.session = session

    def execute(self) -> str:
        count = len(self.session.get_history())
        return f"Calculations in history: {count}"
