# Design Patterns and Statistics Calculator

A Python command-line calculator developed through six cumulative learning stages for IS218. The project uses composition, the Simple Factory pattern, and the Command pattern to separate mathematical operations, object creation, application actions, and user interaction.

## Features

- Arithmetic: addition, subtraction, multiplication, division, and modulo
- Additional operations: absolute difference, square, square root, power, scaling, and sum
- Mean and standard deviation using pandas
- CSV input with configurable column selection
- History containing only successful calculations
- Commands to view history, count results, display summaries, and clear session data
- Independent request processing that continues after expected failures
- Numeric validation and error handling
- 208 automated tests and a GitHub Actions testing workflow

## Setup

Run these commands in WSL, Linux, or macOS:

git clone https://github.com/dlg309/Design-Patterns-Stats-Calculator.git
cd Design-Patterns-Stats-Calculator
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

## Run the Calculator

python -m calculator

Example commands:

add 2 3
power 3 exponent=4
scale 12 factor=3
sum 10 20 30
mean 10 20 30 40 50
stddev 10 20 30 40 50
stddev 2 4 6 ddof=0
csv mean values.csv
csv stddev values.csv ddof=0
history
count
summary
clear
help
exit

Standard deviation defaults to sample deviation (`ddof=1`).
Use `ddof=0` for population deviation. Both require at least
two observations.

CSV files use a column named `value` by default. To select
another column:

csv mean scores.csv column=score

The CLI uses whitespace-separated input, so file paths must
not contain spaces.

## Design

| Component | Responsibility |
|---|---|
| Operations | Provide mathematical functions |
| Calculation | Store operands and options, then execute an operation |
| CalculationFactory | Select an operation and construct a calculation |
| History | Store successful calculations and their results |
| CalculatorSession | Coordinate execution and maintain session state |
| Commands | Perform application actions and return display text |
| CLI | Parse requests, execute commands, and handle expected errors |
| Statistics | Apply pandas calculations with explicit validation |
| CSV reader | Extract observations from a selected column |
| Sequence helpers | Process multiple items independently |

Constructing a calculation does not execute its arithmetic.
Execution happens when `get_result()` is called.

History and errors are stored in memory for the current session.
The `clear` command resets both successful history and recorded
failures. Returned history lists are copies, but the calculation
objects inside them remain shared.

## Learning Stages

Each branch preserves a cumulative checkpoint.

| Part | Branch | Focus |
|---|---|---|
| 1 | `part-1-refactoring` | Composition, static operations, validation, and history |
| 2 | `part-2-factory` | Centralized calculation creation |
| 3 | `part-3-flexible-inputs` | Variable operands and named options |
| 4 | `part-4-commands` | Session management, commands, and interactive CLI |
| 5 | `part-5-statistics-csv` | Pandas statistics and CSV input |
| 6 | `part-6-transfer` | Independent request processing and session summaries |

The `main` branch contains the completed application.

## Testing

Run the test suite:

python -m pytest -q

The completed six-part implementation passes 208 tests.
GitHub Actions runs the tests on pushes and pull requests.

## Course Reference

Developed while following the IS218 Command, Simple Factory,
and statistics lessons:

https://github.com/kaw393939/is218-command-factory-statistics

## Author

Diego Guevara  
New Jersey Institute of Technology  
IS218