import vampytest

from ...adventure_core import TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS, Target

from ..target_suggesting import get_best_matching_target


def _iter_options():
    yield (
        (
            TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        None,
        None,
    )
    
    yield (
        (
            TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        'potato',
        None,
    )
    
    yield (
        (
            TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        format(TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, 'x'),
        TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION],
    )
    
    yield (
        (
            TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        'onion',
        TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_best_matching_target(target_ids, value):
    """
    Tests whether ``get_best_matching_target`` works as intended.
    
    Parameters
    ----------
    target_ids : `tuple<int>`
        Target identifiers to filter from.
    
    value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : ``None | Target``
    """
    output = get_best_matching_target(target_ids, value)
    vampytest.assert_instance(output, Target, nullable = True)
    return output
    
