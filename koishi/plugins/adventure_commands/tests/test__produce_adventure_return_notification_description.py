from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...adventure_core import (
    Adventure, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION
)

from ..component_builders import produce_adventure_return_notification_description


def _iter_options():
    adventure = Adventure(
        202509080000,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        0,
        100,
        100,
    )
    
    adventure.updated_at = DateTime(2016, 5, 14, 3, 20, 19, tzinfo = TimeZone.utc)
    adventure.energy_exhausted = 20
    
    yield (
        adventure,
        (
            f'You are recovering for 40 minutes, until <t:{adventure.updated_at.timestamp() + 2400:.0f}:T>.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_return_notification_description(adventure):
    """
    Tests whether ``produce_adventure_return_notification_description`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_return_notification_description(adventure)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
