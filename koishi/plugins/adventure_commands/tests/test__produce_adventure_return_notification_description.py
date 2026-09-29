import vampytest

from ...adventure_core import (
    LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, adventure_create
)

from ..content_building import produce_adventure_return_notification_description


def _iter_options():
    adventure = adventure_create(
        202509080000,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        None,
        0,
        100,
        100,
    )
    
    adventure.updated_at = 1463184000 + 3 * 3600 + 20 * 60 + 19
    adventure.energy_exhausted = 20
    
    yield (
        adventure,
        (
            f'You are recovering for 40 minutes, until <t:{adventure.updated_at + 2400}:T>.'
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
