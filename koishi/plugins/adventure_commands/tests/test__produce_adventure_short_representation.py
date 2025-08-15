from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...adventure_core import (
    Adventure, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS
)

from ..component_builders import produce_adventure_short_representation


def _iter_options():
    adventure = Adventure(
        202508060020,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        adventure,
        (
            f'2016-05-14 00:00:00 UTC {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
            f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
        ),
    )
    
    adventure = Adventure(
        202508060021,
        9999,
        9999,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        adventure,
        '2016-05-14 00:00:00 UTC unknown for unknown',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_short_representation(adventure):
    """
    Tests whether ``produce_adventure_short_representation`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce short representation for.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_short_representation(adventure)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
