from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Component, create_button, create_row, create_separator, create_text_display

from ...adventure_core import (
    ADVENTURE_STATE_FINALIZED, Adventure, LOCATIONS, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, TARGETS,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION
)

from ..component_builders import build_adventure_return_notification_components


def _iter_options():
    adventure_entry_id = 9998
    user_id = 202508140002
    
    adventure = Adventure(
        user_id,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        0,
        100,
        100,
    )
    adventure.energy_exhausted = 10
    adventure.created_at = DateTime(2016, 5, 13, tzinfo = TimeZone.utc)
    adventure.state = ADVENTURE_STATE_FINALIZED
    adventure.action_count = 2
    adventure.entry_id = adventure_entry_id
    
    yield (
        adventure,
        [            
            create_text_display(
                f'### You have returned from adventure at {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
            ),
            create_separator(),
            create_row(
                create_button(
                    'View adventure',
                    enabled = True,
                    custom_id = f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{False:x}.{0:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_return_notification_components(adventure):
    """
    Tests whether ``build_adventure_return_notification_components`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure the user returned from.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_adventure_return_notification_components(adventure)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
