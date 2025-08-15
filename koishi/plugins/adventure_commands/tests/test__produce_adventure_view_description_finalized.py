from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...adventure_core import Adventure

from ..component_builders import produce_adventure_view_description_finalized


def _iter_options():
    adventure = Adventure(
        202508030003,
        0,
        0,
        0,
        0,
        0,
        130,
        140,
    )
    adventure.created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    adventure.updated_at = DateTime(2016, 5, 14, 5, 30, 0, tzinfo = TimeZone.utc)
    adventure.health_exhausted = 20
    adventure.energy_exhausted = 30
    
    yield (
        adventure,
        (
            'Departed at: 2016-05-14 00:00:00 UTC\n'
            'Used health: 20 / 130\n'
            'Used energy: 30 / 140\n'
            'Total duration: 5 hours, 30 minutes\n'
            'Recovery time: 6 hours, 20 minutes'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_view_description_finalized(adventure):
    """
    Tests whether ``produce_adventure_view_description_finalized`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_view_description_finalized(adventure)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
