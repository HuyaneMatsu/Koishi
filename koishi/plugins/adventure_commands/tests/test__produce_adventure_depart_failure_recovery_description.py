from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..component_builders import produce_adventure_depart_failure_recovery_description


def _iter_options():
    until = DateTime(2016, 5, 14, 3, 20, 19, tzinfo = TimeZone.utc)
    now = DateTime(2016, 5, 14, 3, 10, 18, tzinfo = TimeZone.utc)
    
    yield (
        until,
        now,
        (
            f'You are currently recovering for 10 minutes, 1 second, until <t:{until.timestamp():.0f}:T>.\n'
            f'You cannot go on an adventure in the meantime.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_depart_failure_recovery_description(recovering_until, now):
    """
    Tests whether ``produce_adventure_depart_failure_recovery_description`` works as intended.
    
    Parameters
    ----------
    recovering_until : `DateTine`
        Until when the user is recovering.
    
    now : `DateTime`
        The current time.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_depart_failure_recovery_description(recovering_until, now)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
