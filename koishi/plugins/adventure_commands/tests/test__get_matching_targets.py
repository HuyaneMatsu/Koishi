import vampytest

from ...adventure_core import TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS, Target
from ..target_suggesting import get_matching_targets


def _iter_options():
    yield (
        (
            TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        None,
        [
            TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION],
        ],
    )
    
    yield (
        (
            TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        'potato',
        [],
    )
    
    yield (
        (
            TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        format(TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, 'x'),
        [
            TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION],
        ],
    )
    
    yield (
        (
            TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        'onion',
        [
            TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION],
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_matching_targets(target_ids, value):
    """
    Tests whether ``get_matching_targets`` works as intended.
    
    Parameters
    ----------
    target_ids : `tuple<int>`
        Target identifiers to filter from.
    
    value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : ``list<Target>``
    """
    output = get_matching_targets(target_ids, value)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Target)
    return output
