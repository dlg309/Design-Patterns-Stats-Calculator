import pytest

from calculator.statistics import mean, standard_deviation


def test_mean():
    assert mean([10, 20, 30, 40, 50]) == pytest.approx(30)


def test_mean_accepts_one_value():
    assert mean([7]) == 7.0


def test_mean_rejects_empty_input():
    with pytest.raises(ValueError, match="at least one value"):
        mean([])


def test_sample_standard_deviation_is_default():
    assert standard_deviation([2, 4, 6]) == pytest.approx(2)


def test_population_standard_deviation():
    assert standard_deviation([2, 4, 6], ddof=0) == pytest.approx(
        (8 / 3) ** 0.5
    )


def test_identical_values_have_zero_deviation():
    assert standard_deviation([5, 5, 5]) == 0.0


@pytest.mark.parametrize("values", [[], [7]])
@pytest.mark.parametrize("ddof", [0, 1])
def test_standard_deviation_requires_two_values(values, ddof):
    with pytest.raises(ValueError, match="at least two values"):
        standard_deviation(values, ddof=ddof)


@pytest.mark.parametrize("ddof", [-1, 2, 0.5])
def test_standard_deviation_rejects_unsupported_ddof(ddof):
    with pytest.raises(ValueError, match="ddof must be"):
        standard_deviation([2, 4, 6], ddof=ddof)


@pytest.mark.parametrize("operation", [mean, standard_deviation])
@pytest.mark.parametrize(
    "bad_value",
    ["hello", None, float("nan"), float("inf")],
)
def test_statistics_reject_invalid_observations(operation, bad_value):
    with pytest.raises(ValueError):
        operation([2, bad_value, 6])


@pytest.mark.parametrize("operation", [mean, standard_deviation])
def test_statistics_accept_numeric_strings(operation):
    assert operation(["2", "4", "6"]) == pytest.approx(
        operation([2, 4, 6])
    )
