import vampytest
from hata import Component, create_separator, create_text_display

from ...adventure_core import (
    AUTO_CANCELLATIONS, AUTO_CANCELLATION_ID_NEVER, LOCATIONS, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
    RETURNS, RETURN_ID_AFTER, TARGETS, TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION
)

from ..component_builders import build_adventure_create_cancel_components


def _iter_options():
    location_id = LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS
    target_id = TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION
    return__id = RETURN_ID_AFTER
    auto_cancellation_id = AUTO_CANCELLATION_ID_NEVER
    duration = 3600 * 4
    
    yield (
        LOCATIONS[location_id],
        TARGETS[target_id],
        duration,
        RETURNS[return__id],
        AUTO_CANCELLATIONS[auto_cancellation_id],
        [
            create_text_display('### You have cancelled departing, stay safe wise adventurer!'),
            create_separator(),
            create_text_display(
                'Location: Human village outskirts\n'
                'Target: Gardening (Scarlet onions)\n'
                'Duration: 4h\n'
                'Return: After\n'
                'Auto-cancellation: Never (none)'
            ),
        ]
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_create_cancel_components(
    location, target, duration, return_, auto_cancellation
):
    """
    Tests whether ``build_adventure_create_cancel_components`` works as intended.
    
    Parameters
    ----------
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
    output = build_adventure_create_cancel_components(
        location, target, duration, return_, auto_cancellation
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
