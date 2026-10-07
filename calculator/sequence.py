"""Process prepared calculations independently."""


def execute_sequence(session, calculations):
    results = []
    errors = []

    for calculation in calculations:
        try:
            result = session.calculate(calculation)
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            session.record_failure(error)
            errors.append(str(error))
        else:
            results.append(result)

    return results, errors


def execute_requests(session, requests):
    """Prepare and execute name/values/options requests independently."""
    from calculator.factory import CalculationFactory

    results = []
    errors = []

    for name, values, options in requests:
        try:
            calculation = CalculationFactory.create(
                name, *values, **options
            )
            result = session.calculate(calculation)
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            session.record_failure(error)
            errors.append(str(error))
        else:
            results.append(result)

    return results, errors
