import pytest

from calculator.calculation import Calculation
from calculator.history import History
from calculator.operations import Operations


def test_history_starts_empty():
    history = History()
    assert history.get_history() == []


def test_history_stores_calculation_and_result():
    history = History()
    calculation = Calculation([2, 3], Operations.add)
    result = calculation.get_result()

    history.add(calculation, result)

    assert history.get_history() == [(calculation, 5.0)]


def test_changing_returned_list_does_not_change_history():
    history = History()
    calculation = Calculation([2, 3], Operations.add)
    history.add(calculation, calculation.get_result())

    copied_entries = history.get_history()
    copied_entries.clear()

    assert history.get_history() == [(calculation, 5.0)]


def test_clear_removes_entries():
    history = History()
    calculation = Calculation([2, 3], Operations.add)
    history.add(calculation, calculation.get_result())

    history.clear()

    assert history.get_history() == []


def test_history_rejects_non_calculation_objects():
    history = History()

    with pytest.raises(TypeError, match="Calculation objects only"):
        history.add("not a calculation", 5)


def test_history_does_not_rerun_operation():
    calls = []

    def tracked_add(a, b):
        calls.append((a, b))
        return a + b

    history = History()
    calculation = Calculation([2, 3], tracked_add)
    result = calculation.get_result()

    history.add(calculation, result)
    history.get_history()

    assert calls == [(2.0, 3.0)]


def test_separate_histories_do_not_share_entries():
    first = History()
    second = History()
    calculation = Calculation([2, 3], Operations.add)

    first.add(calculation, calculation.get_result())

    assert second.get_history() == []
