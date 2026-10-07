"""Parse requests and run the interactive calculator."""

from calculator.commands import (
    CalculateCommand,
    ClearHistoryCommand,
    CountCommand,
    HelpCommand,
    HistoryCommand,
    SummaryCommand,
)
from calculator.factory import CalculationFactory
from calculator.inputs import read_csv_values
from calculator.session import CalculatorSession


def parse_arguments(tokens):
    values = []
    options = {}

    for token in tokens:
        if "=" in token:
            key, value = token.split("=", 1)

            if not key or not value:
                raise ValueError("Options must use key=value.")

            if key in options:
                raise ValueError(f"Duplicate option: {key}")

            options[key] = value
        else:
            values.append(token)

    return values, options


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

    if name == "summary":
        if len(parts) != 1:
            raise ValueError("summary does not accept arguments.")
        return SummaryCommand(session)

    if name == "csv":
        if len(parts) < 3:
            raise ValueError("Usage: csv mean|stddev PATH [column=NAME] [ddof=0|1]")

        operation = parts[1].lower()
        if operation not in ("mean", "stddev"):
            raise ValueError("CSV supports mean and stddev only.")

        extra_values, options = parse_arguments(parts[3:])
        if extra_values:
            raise ValueError("CSV settings must use key=value.")

        column = options.pop("column", "value")
        values = read_csv_values(parts[2], column=column)
        calculation = CalculationFactory.create(
            operation, *values, **options
        )
        return CalculateCommand(session, calculation)

    if name not in CalculationFactory.operations:
        raise ValueError(f"Unknown command: {name}")

    values, options = parse_arguments(parts[1:])
    calculation = CalculationFactory.create(name, *values, **options)
    return CalculateCommand(session, calculation)


def run():
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

        except (ValueError, TypeError, ArithmeticError, OSError) as error:
            session.record_failure(error)
            print(f"Error: {error}")
