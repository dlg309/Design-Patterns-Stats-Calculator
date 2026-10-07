import pandas as pd
import pytest

from calculator.factory import CalculationFactory
from calculator.inputs import read_csv_values


def test_read_csv_values(tmp_path):
    path = tmp_path / "values.csv"
    path.write_text("value\n10\n20\n30\n")

    assert read_csv_values(path) == [10, 20, 30]


def test_reader_selects_value_column(tmp_path):
    path = tmp_path / "values.csv"
    path.write_text("label,value\nfirst,10\nsecond,20\n")

    assert read_csv_values(path) == [10, 20]


def test_reader_rejects_missing_header(tmp_path):
    path = tmp_path / "values.csv"
    path.write_text("score\n10\n20\n")

    with pytest.raises(ValueError, match="column named value"):
        read_csv_values(path)


def test_reader_reports_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_csv_values(tmp_path / "missing.csv")


def test_reader_rejects_empty_file(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("")

    with pytest.raises(pd.errors.EmptyDataError):
        read_csv_values(path)


def test_reader_rejects_malformed_csv(tmp_path):
    path = tmp_path / "broken.csv"
    path.write_text('value\n"unterminated\n')

    with pytest.raises(pd.errors.ParserError):
        read_csv_values(path)


@pytest.mark.parametrize("observation", ["hello", '""', "inf"])
def test_bad_csv_observations_fail_numeric_validation(tmp_path, observation):
    path = tmp_path / "values.csv"
    path.write_text(f"value\n10\n{observation}\n30\n")

    values = read_csv_values(path)

    with pytest.raises(ValueError):
        CalculationFactory.create("mean", *values)


def test_header_only_csv_fails_when_mean_executes(tmp_path):
    path = tmp_path / "values.csv"
    path.write_text("value\n")

    values = read_csv_values(path)
    calculation = CalculationFactory.create("mean", *values)

    with pytest.raises(ValueError, match="at least one value"):
        calculation.get_result()


@pytest.mark.parametrize("operation", ["mean", "stddev"])
def test_csv_and_direct_values_produce_same_result(tmp_path, operation):
    path = tmp_path / "values.csv"
    path.write_text("value\n2\n4\n6\n")

    from_csv = CalculationFactory.create(
        operation, *read_csv_values(path)
    )
    direct = CalculationFactory.create(operation, 2, 4, 6)

    assert from_csv.get_result() == pytest.approx(direct.get_result())


def test_reader_selects_alternate_column(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text("value,score\n100,2\n200,4\n300,6\n")

    assert read_csv_values(path, column="score") == [2, 4, 6]


def test_reader_rejects_missing_selected_column(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text("value\n2\n4\n")

    with pytest.raises(ValueError, match="column named score"):
        read_csv_values(path, column="score")
