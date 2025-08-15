from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...adventure_core import ADVENTURE_STATE_ACTIONING, Adventure

from ..component_builders import produce_adventure_view_description_active


def _iter_options():
    adventure = Adventure(
        202508030002,
        0,
        0,
        0,
        0,
        0,
        130,
        140,
    )
    adventure.created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    adventure.health_exhausted = 20
    adventure.energy_exhausted = 30
    adventure.state = ADVENTURE_STATE_ACTIONING
    
    yield (
        adventure,
        DateTime(2016, 5, 14, 5, 30, tzinfo = TimeZone.utc),
        45000,
        20000,
        (
            'Departed at: 2016-05-14 00:00:00 UTC\n'
            'Used health: 20 / 130\n'
            'Used energy: 30 / 140\n'
            'Used inventory: 20.000 / 45.000 kg\n'
            'Elapsed time: 5 hours, 30 minutes\n'
            'You are currently working on your target task.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_view_description_active(adventure, now, inventory_total, inventory_exhausted):
    """
    Tests whether ``produce_adventure_view_description_active`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    now : `DateTime`
        The current time.
    
    inventory_total : `int`
        The user's total inventory.
    
    inventory_exhausted : `int`
        The user's used inventory.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_view_description_active(adventure, now, inventory_total, inventory_exhausted)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
