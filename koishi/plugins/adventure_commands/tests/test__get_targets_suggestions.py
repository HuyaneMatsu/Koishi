import vampytest

from ...adventure_core import TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS, Target

from ..target_suggesting import get_target_suggestions


def _iter_options():
    yield (
        (
            TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        None,
        [
            (
                TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name,
                format(TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, 'x'),
            ),
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
            (
                TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name,
                format(TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, 'x'),
            ),
        ],
    )
    
    yield (
        (
            TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        'onion',
        [
            (
                TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name,
                format(TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, 'x'),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_target_suggestions(target_ids, value):
    """
    Tests whether ``get_target_suggestions`` works as intended.
    
    Parameters
    ----------
    target_ids : `tuple<int>`
        Target identifiers to filter from.
    
    value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : ``list<(str, str)>``
    """
    output = get_target_suggestions(target_ids, value)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, tuple)
        vampytest.assert_eq(len(element), 2)
        vampytest.assert_instance(element[0], str)
        vampytest.assert_instance(element[1], str)
    return output
