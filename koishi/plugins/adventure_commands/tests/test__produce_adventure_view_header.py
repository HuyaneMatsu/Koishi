import vampytest

from ...adventure_core import (
    Adventure, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS
)

from ..component_builders import produce_adventure_view_header


def _iter_options():
    adventure = Adventure(
        202508030000,
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
            f'### Adventure to {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
            f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
        ),
    )
    
    adventure = Adventure(
        202508030001,
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
        '### Adventure to unknown for unknown',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_view_header(adventure):
    """
    Tests whether ``produce_adventure_view_header`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce header for.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_view_header(adventure)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
