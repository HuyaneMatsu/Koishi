import vampytest

from ...adventure_core import (
    Adventure, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS
)

from ..component_builders import produce_adventure_return_notification_header


def _iter_options():
    adventure = Adventure(
        202508140000,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        0,
        0,
        0,
    )
    
    yield (
        adventure,
        (
            f'### You have returned from adventure at {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
            f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
        ),
    )
    
    adventure = Adventure(
        202508140001,
        9999,
        9999,
        0,
        0,
        0,
        0,
        0,
    )
    
    yield (
        adventure,
        '### You have returned from adventure at unknown for unknown',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_return_notification_header(adventure):
    """
    Tests whether ``produce_adventure_return_notification_header`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce header for.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_return_notification_header(adventure)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
