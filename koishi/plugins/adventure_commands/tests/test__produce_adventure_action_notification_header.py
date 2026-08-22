from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...adventure_core import (
    Adventure, AdventureAction, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS,
    ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS
)

from ..content_building import produce_adventure_action_notification_header


def _iter_options():
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    adventure_entry_id = 9993
    
    adventure = Adventure(
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
    
    adventure_action = AdventureAction(
        adventure_entry_id,
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        created_at,
        None,
        None,
        0,
        10,
    )
    
    yield (
        adventure,
        adventure_action,
        (
            f'### Gardening at {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
            f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
        ),
    )
    
    adventure_entry_id = 9993
    
    adventure = Adventure(
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
    
    adventure_action = AdventureAction(
        adventure_entry_id,
        999999,
        created_at,
        None,
        None,
        0,
        10,
    )
    
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
