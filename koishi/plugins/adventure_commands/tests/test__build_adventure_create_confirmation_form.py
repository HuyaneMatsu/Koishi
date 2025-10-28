import vampytest
from hata import ButtonStyle, InteractionForm, create_button, create_row, create_separator, create_text_display

from ...adventure_core import (
    AUTO_CANCELLATIONS, AUTO_CANCELLATION_ID_NEVER, LOCATIONS, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
    RETURNS, RETURN_ID_AFTER, TARGETS, TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION
)

from ..component_builders import build_adventure_create_confirmation_form


def _iter_options():
    user_id = 202507220000
    location_id = LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS
    target_id = TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION
    return__id = RETURN_ID_AFTER
    auto_cancellation_id = AUTO_CANCELLATION_ID_NEVER
    duration = 3600 * 4
    
    yield (
        user_id,
        LOCATIONS[location_id],
        TARGETS[target_id],
        duration,
        RETURNS[return__id],
        AUTO_CANCELLATIONS[auto_cancellation_id],
        True,
        InteractionForm(
            'Confirm your adventure',
            [
                create_text_display(
                    'Location: Human village outskirts\n'
                    'Target: Gardening (Scarlet onions)\n'
                    'Duration: 4h\n'
                    'Return: After\n'
                    'Auto-cancellation: Never (none)'
                ),
            ],
            (
                f'adventure.create.1.{user_id:x}.{location_id:x}.{target_id:x}.'
                f'{duration:x}.{return__id:x}.{auto_cancellation_id:x}'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_create_confirmation_form(
    user_id, location, target, duration, return_, auto_cancellation, enable_interactive_components
):
    """
    Tests whether ``build_adventure_create_confirmation_form`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
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
    
    enable_interactive_components : `bool`
        Whether interaction components should be enabled.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    output = build_adventure_create_confirmation_form(
        user_id, location, target, duration, return_, auto_cancellation, enable_interactive_components
    )
    vampytest.assert_instance(output, InteractionForm)
    return output
