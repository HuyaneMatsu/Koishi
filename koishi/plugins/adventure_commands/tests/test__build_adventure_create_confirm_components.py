import vampytest
from hata import Component, create_button, create_row, create_separator, create_text_display

from ...adventure_core import (
    AUTO_CANCELLATIONS, AUTO_CANCELLATION_ID_NEVER, LOCATIONS, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
    RETURNS, RETURN_ID_AFTER, TARGETS, TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION
)

from ..component_builders import build_adventure_create_confirm_components


def _iter_options():
    user_id = 202508130001
    adventure_entry_id = 8888
    location_id = LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS
    target_id = TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION
    return_id = RETURN_ID_AFTER
    auto_cancellation_id = AUTO_CANCELLATION_ID_NEVER
    duration = 3600 * 4
    
    yield (
        user_id,
        adventure_entry_id,
        LOCATIONS[location_id],
        TARGETS[target_id],
        duration,
        RETURNS[return_id],
        AUTO_CANCELLATIONS[auto_cancellation_id],
        [
            create_text_display('### You began your adventure, best of luck brave adventurer!'),
            create_separator(),
            create_text_display(
                'Location: Human village outskirts\n'
                'Target: Gardening (Scarlet onions)\n'
                'Duration: 4h\n'
                'Return: After\n'
                'Auto-cancellation: Never (none)'
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
def test__build_adventure_create_confirm_components(
    user_id, adventure_entry_id, location, target, duration, return_, auto_cancellation
):
    """
    Tests whether ``build_adventure_create_confirm_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    adventure_entry_id : `int`
        The adventure's entries identifier in the database.
    
    location : ``Location``
        Target duration.
    
    target : ``Target``
        Target action set.
    
    duration : `int`
        Duration.
    
    return_ : ``Return``
        Return logic identifier.
    
    auto_cancellation : ``AutoCancellation``
        Auto cancellation.
    
    Returns
    -------
    components : ``list<Component>``
    """
    output = build_adventure_create_confirm_components(
        user_id, adventure_entry_id, location, target, duration, return_, auto_cancellation
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
