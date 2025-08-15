import vampytest

from ...adventure_core import (
    Adventure, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS
)

from ..component_builders import produce_adventure_action_listing_view_header


def _iter_options():
    adventure = Adventure(
        202508060010,
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
        0,
        (
            f'### Actions of {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
            f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name} (page 1)'
        ),
    )
    
    adventure = Adventure(
        202508060011,
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
        100,
        '### Actions of unknown for unknown (page 101)',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_action_listing_view_header(adventure, page_index):
    """
    Tests whether ``produce_adventure_action_listing_view_header`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce header for.
    
    page_index : `int`
        The shown page's index.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_action_listing_view_header(adventure, page_index)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
