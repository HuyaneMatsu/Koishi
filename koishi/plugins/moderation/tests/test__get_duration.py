from datetime import timedelta as TimeDelta

import vampytest

from ..shared_helpers_mute import DURATION_MAX, get_duration


def test__get_duration__zeros():
    """
    Tests whether ``get_duration`` works as intended.
    
    Case: Only zeros.
    """
    output = get_duration(0, 0, 0, 0)
    
    vampytest.assert_instance(output, TimeDelta)
    vampytest.assert_eq(output, DURATION_MAX)


def test__get_duration__actual():
    """
    Tests whether ``get_duration`` works as intended.
    
    Case: Actual value.
    """
    output = get_duration(2, 3, 4, 5)
    expected_output = TimeDelta(days = 2, hours = 3, minutes = 4, seconds = 5)
    
    vampytest.assert_instance(output, TimeDelta)
    vampytest.assert_eq(output, expected_output)


def test__get_duration__over_limit():
    """
    Tests whether ``get_duration`` works as intended.
    
    Case: Over limit.
    """
    output = get_duration(200, 0, 0, 0)
    
    vampytest.assert_instance(output, TimeDelta)
    vampytest.assert_eq(output, DURATION_MAX)
