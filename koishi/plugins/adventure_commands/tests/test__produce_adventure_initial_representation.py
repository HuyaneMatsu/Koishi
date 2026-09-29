import vampytest

from ...adventure_core import (
    AUTO_CANCELLATIONS, AUTO_CANCELLATION_ID_NEVER, LOCATIONS, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
    RETURNS, RETURN_ID_AFTER, TARGETS, TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
    goal_create_item_exact
)
from ...item_core import get_item_nullable, ITEM_ID_PEACH
from ...unit_core import AMOUNT_TYPE_COUNT

from ..content_building import produce_adventure_initial_representation


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    yield (
        LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS],
        TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION],
        3600 * 4,
        RETURNS[RETURN_ID_AFTER],
        AUTO_CANCELLATIONS[AUTO_CANCELLATION_ID_NEVER],
        None,
        (
            'Location: Human village outskirts\n'
            'Target: Gardening (Scarlet onions)\n'
            'Duration: 4 hours\n'
            'Return: After\n'
            'Auto-cancellation: Never (none)'
        ),
    )
    
    yield (
        LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS],
        TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION],
        3600 * 4,
        RETURNS[RETURN_ID_AFTER],
        AUTO_CANCELLATIONS[AUTO_CANCELLATION_ID_NEVER],
        goal_create_item_exact(item_peach.id, AMOUNT_TYPE_COUNT, 20),
        (
            f'Location: Human village outskirts\n'
            f'Target: Gardening (Scarlet onions)\n'
            f'Duration: 4 hours\n'
            f'Return: After\n'
            f'Auto-cancellation: Never (none)\n'
            f'Goal: 20 {item_peach.emoji} {item_peach.name}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_initial_representation(location, target, duration, return_, auto_cancellation, goal):
    """
    Tests whether ``produce_adventure_initial_representation`` works as intended.
    
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
    
    goal : ``None | Goal``
        The goal of the adventure.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_initial_representation(location, target, duration, return_, auto_cancellation, goal)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
