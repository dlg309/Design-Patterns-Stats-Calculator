import pytest

from calculator.calculation import Calculation
from calculator.factory import CalculationFactory


@pytest.mark.parametrize(
    "name, a, b, expected",
    [
        ("add", 2, 3, 5),
        ("subtract", 8, 3, 5),
        ("multiply", 4, 3, 12),
        ("divide", 9, 2, 4.5),
        ("absolute_difference", 2, 8, 6),
    ],
)
def test_factory_creates_calculations(name, a, b, expected):
    calculation = CalculationFactory.create(name, a, b)

    assert isinstance(calculation, Calculation)
    assert calculation.get_result() == pytest.approx(expected)


def test_factory_normalizes_operation_name():
    calculation = CalculationFactory.create(" ADD ", "2", "3")

    assert calculation.get_result() == 5.0


def test_factory_rejects_unknown_operation():
    with pytest.raises(ValueError, match="Unknown operation: missing"):
        CalculationFactory.create("missing", 2, 3)


def test_factory_preserves_operand_validation_error():
    with pytest.raises(ValueError, match="must be a number"):
        CalculationFactory.create("add", "hello", 3)


def test_factory_defers_division_until_execution():
    calculation = CalculationFactory.create("divide", 5, 0)

    with pytest.raises(ZeroDivisionError):
        calculation.get_result()


def test_factory_does_not_execute_operation(monkeypatch):
    calls = []

    def tracked_add(a, b):
        calls.append((a, b))
        return a + b

    monkeypatch.setitem(
        CalculationFactory.operations, "add", tracked_add
    )

    calculation = CalculationFactory.create("add", 2, 3)

    assert calls == []

    assert calculation.get_result() == 5.0
    assert calls == [(2.0, 3.0)]


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 3, 1),
        (12, 4, 0),
        (7.5, 2, 1.5),
    ],
)
def test_factory_supports_modulo(a, b, expected):
    calculation = CalculationFactory.create("modulo", a, b)

    assert calculation.get_result() == pytest.approx(expected)


def test_factory_normalizes_modulo_name():
    calculation = CalculationFactory.create(" MODULO ", 10, 3)

    assert calculation.get_result() == 1.0


def test_modulo_by_zero_fails_during_execution():
    calculation = CalculationFactory.create("modulo", 10, 0)

    with pytest.raises(ZeroDivisionError):
        calculation.get_result()


@pytest.mark.parametrize(
    "name, values, expected",
    [
        ("square", (4,), 16),
        ("sqrt", (9,), 3),
        ("sum", (2, 3, 4), 9),
    ],
)
def test_factory_supports_flexible_inputs(name, values, expected):
    calculation = CalculationFactory.create(name, *values)

    assert calculation.get_result() == pytest.approx(expected)


@pytest.mark.parametrize(
    "name, values",
    [
        ("add", (2,)),
        ("add", (2, 3, 4)),
        ("square", ()),
        ("sqrt", (9, 16)),
    ],
)
def test_factory_rejects_wrong_operand_count(name, values):
    with pytest.raises(ValueError, match="requires exactly"):
        CalculationFactory.create(name, *values)


def test_negative_square_root_fails_during_execution():
    calculation = CalculationFactory.create("sqrt", -1)

    with pytest.raises(ValueError):
        calculation.get_result()


def test_empty_sum_fails_during_execution():
    calculation = CalculationFactory.create("sum")

    with pytest.raises(ValueError, match="at least one value"):
        calculation.get_result()


def test_power_uses_default_exponent():
    calculation = CalculationFactory.create("power", 3)

    assert calculation.get_result() == 9.0


def test_power_accepts_named_exponent():
    calculation = CalculationFactory.create("power", 3, exponent=4)

    assert calculation.get_result() == 81.0


def test_power_converts_numeric_string_option():
    calculation = CalculationFactory.create("power", 3, exponent="4")

    assert calculation.get_result() == 81.0


@pytest.mark.parametrize(
    "name, values, options",
    [
        ("power", (3,), {"unknown": 4}),
        ("add", (2, 3), {"exponent": 4}),
    ],
)
def test_factory_rejects_unsupported_options(name, values, options):
    with pytest.raises(ValueError, match="Unsupported option"):
        CalculationFactory.create(name, *values, **options)


@pytest.mark.parametrize("exponent", ["hello", float("inf"), float("nan")])
def test_power_rejects_invalid_exponent(exponent):
    with pytest.raises(ValueError):
        CalculationFactory.create("power", 3, exponent=exponent)


def test_power_rejects_exponent_as_second_operand():
    with pytest.raises(ValueError, match="requires exactly"):
        CalculationFactory.create("power", 3, 4)


def test_power_domain_error_is_delayed_until_execution():
    calculation = CalculationFactory.create("power", -1, exponent=0.5)

    with pytest.raises(ValueError):
        calculation.get_result()


def test_scale_with_named_factor():
    calculation = CalculationFactory.create("scale", 12, factor=3)

    assert calculation.get_result() == 4.0


def test_scale_default_factor_preserves_value():
    calculation = CalculationFactory.create("scale", 12)

    assert calculation.get_result() == 12.0


def test_scale_rejects_unsupported_option():
    with pytest.raises(ValueError, match="Unsupported option"):
        CalculationFactory.create("scale", 12, exponent=3)


def test_scale_zero_factor_fails_during_execution():
    calculation = CalculationFactory.create("scale", 12, factor=0)

    with pytest.raises(ZeroDivisionError):
        calculation.get_result()
