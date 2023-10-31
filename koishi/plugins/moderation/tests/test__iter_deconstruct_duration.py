from datetime import timedelta as TimeDelta

import vampytest

from ..shared_helpers_mute import iter_deconstruct_duration


def test__iter_deconstruct_duration():
    """
    Tests whether ``iter_deconstruct_duration`` works as intended.
    """
    value = TimeDelta(days = 2, hours = 3, minutes = 4, seconds = 5)
    output = [*iter_deconstruct_duration(value)]
    vampytest.assert_eq(output, [2, 3, 4, 5])
