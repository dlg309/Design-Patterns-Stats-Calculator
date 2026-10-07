"""Convert user input into application commands."""

from calculator.commands import (
    CalculateCommand,
    ClearHistoryCommand,
    CountCommand,
    HelpCommand,
    HistoryCommand,
)
from calculator.factory import CalculationFactory


def prepare_command(line, session):
    parts = line.split()

    if not parts:
        raise ValueError("Enter a command.")

    name = parts[0].lower()

    if name == "help":
        if len(parts) != 1:
            raise ValueError("help does not accept arguments.")
        return HelpCommand()

    if name == "history":
        if len(parts) != 1:
            raise ValueError("history does not accept arguments.")
        return HistoryCommand(session)

    if name == "clear":
        if len(parts) != 1:
            raise ValueError("clear does not accept arguments.")
        return ClearHistoryCommand(session)

    if name == "count":
        if len(parts) != 1:
            raise ValueError("count does not accept arguments.")
        return CountCommand(session)

    if name not in CalculationFactory.operations:
        raise ValueError(f"Unknown command: {name}")

    values = []
    options = {}

    for token in parts[1:]:
        if "=" in token:
            key, value = token.split("=", 1)

            if not key or not value:
                raise ValueError("Options must use key=value.")

            if key in options:
                raise ValueError(f"Duplicate option: {key}")

            options[key] = value
        else:
            values.append(token)

    calculation = CalculationFactory.create(name, *values, **options)
    return CalculateCommand(session, calculation)


def run():
    from calculator.session import CalculatorSession

    session = CalculatorSession()
    print("Calculator ready. Type help for commands or exit to quit.")

    while True:
        try:
            line = input("> ").strip()

            if not line:
                continue

            if line.lower() == "exit":
                print("Goodbye!")
                break

            command = prepare_command(line, session)
            print(command.execute())

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        except (ValueError, TypeError, ArithmeticError) as error:
            print(f"Error: {error}")
