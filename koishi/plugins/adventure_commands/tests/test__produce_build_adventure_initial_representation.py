import vampytest

from ...adventure_core import (
    AUTO_CANCELLATIONS, AUTO_CANCELLATION_ID_NEVER, LOCATIONS, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
    RETURNS, RETURN_ID_AFTER, TARGETS, TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION
)

from ..component_builders import produce_adventure_initial_representation


def _iter_options():
    yield (
        LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS],
        TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION],
        3600 * 4,
        RETURNS[RETURN_ID_AFTER],
        AUTO_CANCELLATIONS[AUTO_CANCELLATION_ID_NEVER],
        (
            'Location: Human village outskirts\n'
            'Target: Gardening (Scarlet onions)\n'
            'Duration: 4h\n'
            'Return: After\n'
            'Auto-cancellation: Never (none)'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_initial_representation(location, target, duration, return_, auto_cancellation):
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
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_initial_representation(location, target, duration, return_, auto_cancellation)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
