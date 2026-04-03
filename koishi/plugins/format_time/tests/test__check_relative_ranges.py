import vampytest
from hata.ext.slash import InteractionAbortedError

from ..constants import (
    RELATIVE_DAYS_MAX, RELATIVE_DAYS_MIN, RELATIVE_HOURS_MAX, RELATIVE_HOURS_MIN, RELATIVE_MINUTES_MAX,
    RELATIVE_MINUTES_MIN, RELATIVE_MONTHS_MAX, RELATIVE_MONTHS_MIN, RELATIVE_SECONDS_MAX, RELATIVE_SECONDS_MIN,
    RELATIVE_WEEKS_MAX, RELATIVE_WEEKS_MIN, RELATIVE_YEARS_MAX, RELATIVE_YEARS_MIN
)

from ..helpers import check_relative_ranges


def _iter_options__passing():
    yield 'years', RELATIVE_YEARS_MIN
    yield 'years', RELATIVE_YEARS_MAX
    
    yield 'months', RELATIVE_MONTHS_MIN
    yield 'months', RELATIVE_MONTHS_MAX
    
    yield 'weeks', RELATIVE_WEEKS_MIN
    yield 'weeks', RELATIVE_WEEKS_MAX
    
    yield 'days', RELATIVE_DAYS_MIN
    yield 'days', RELATIVE_DAYS_MAX
    
    yield 'hours', RELATIVE_HOURS_MIN
    yield 'hours', RELATIVE_HOURS_MAX
    
    yield 'minutes', RELATIVE_MINUTES_MIN
    yield 'minutes', RELATIVE_MINUTES_MAX
    
    yield 'seconds', RELATIVE_SECONDS_MIN
    yield 'seconds', RELATIVE_SECONDS_MAX


def _iter_options__abortion():
    yield 'years', RELATIVE_YEARS_MIN - 1
    yield 'years', RELATIVE_YEARS_MAX + 1
    
    yield 'months', RELATIVE_MONTHS_MIN - 1
    yield 'months', RELATIVE_MONTHS_MAX + 1
    
    yield 'weeks', RELATIVE_WEEKS_MIN - 1
    yield 'weeks', RELATIVE_WEEKS_MAX + 1
    
    yield 'days', RELATIVE_DAYS_MIN - 1
    yield 'days', RELATIVE_DAYS_MAX + 1
    
    yield 'hours', RELATIVE_HOURS_MIN - 1
    yield 'hours', RELATIVE_HOURS_MAX + 1
    
    yield 'minutes', RELATIVE_MINUTES_MIN - 1
    yield 'minutes', RELATIVE_MINUTES_MAX + 1
    
    yield 'seconds', RELATIVE_SECONDS_MIN - 1
    yield 'seconds', RELATIVE_SECONDS_MAX + 2


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__abortion()).raising(InteractionAbortedError))
def test__check_relative_ranges(parameter_name, parameter_value):
    """
    Tests whether ```check_relative_ranges`` works as intended.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter's name to modify.
    
    parameter_value : `int`
        New parameter value.
    """
    keyword_parameters = {parameter_name: parameter_value}
    keyword_parameters.setdefault('years', 0)
    keyword_parameters.setdefault('months', 0)
    keyword_parameters.setdefault('weeks', 0)
    keyword_parameters.setdefault('days', 0)
    keyword_parameters.setdefault('hours', 0)
    keyword_parameters.setdefault('minutes', 0)
    keyword_parameters.setdefault('seconds', 0)
    
    check_relative_ranges(**keyword_parameters)
