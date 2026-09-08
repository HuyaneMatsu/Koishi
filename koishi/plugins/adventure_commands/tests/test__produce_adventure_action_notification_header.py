import vampytest

from ...adventure_core import (
    LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS, ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS, adventure_action_create, adventure_create
)

from ..content_building import produce_adventure_action_notification_header


def _iter_options():
    created_at = 1463184000
    adventure_entry_id = 9993
    
    adventure_action = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        created_at,
        None,
        None,
        0,
        10,
    )
    
    adventure = adventure_create(
        202608190000,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.entry_id = adventure_entry_id
    adventure.action_listing = [adventure]
    
    yield (
        adventure,
        adventure_action,
        (
            f'### Gardening at {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
            f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
        ),
    )
    
    adventure_entry_id = 9993
    
    adventure_action = adventure_action_create(
        999999,
        created_at,
        None,
        None,
        0,
        10,
    )
    
    adventure = adventure_create(
        202608190001,
        9999,
        9999,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.entry_id = adventure_entry_id
    adventure.action_listing = [adventure]
    
    yield (
        adventure,
        adventure_action,
        '### Unknown at unknown for unknown',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_action_notification_header(adventure, adventure_action):
    """
    Tests whether ``produce_adventure_action_notification_header`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure the user is on.
    
    adventure_action : ``AdventureAction``
        The adventure action to display.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_action_notification_header(adventure, adventure_action)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
