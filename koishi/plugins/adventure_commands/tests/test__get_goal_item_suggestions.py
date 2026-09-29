import vampytest

from ...adventure_core import ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION
from ...item_core import ITEM_ID_FROG, ITEM_ID_SCARLET_ONION, ITEM_ID_STRAW_HAT, get_item_nullable

from ..goal_item_suggesting import get_goal_item_suggestions


def _iter_options():
    item_scarlet_onion = get_item_nullable(ITEM_ID_SCARLET_ONION)
    assert item_scarlet_onion is not None
    
    item_frog = get_item_nullable(ITEM_ID_FROG)
    assert item_frog is not None
    
    item_straw_hat = get_item_nullable(ITEM_ID_STRAW_HAT)
    assert item_straw_hat is not None
    
    yield (
        (
            ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        None,
        [
            (item_frog.name, format(item_frog.id, 'x')),
            (item_scarlet_onion.name, format(item_scarlet_onion.id, 'x')),
            (item_straw_hat.name, format(item_straw_hat.id, 'x')),
        ],
    )
    
    yield (
        (
            ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        format(item_scarlet_onion.id, 'x'),
        [
            (item_scarlet_onion.name, format(item_scarlet_onion.id, 'x')),
        ],
    )
    
    yield (
        (
            ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        'onion',
        [
            (item_scarlet_onion.name, format(item_scarlet_onion.id, 'x')),
        ],
    )
    
    yield (
        (
            ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        ),
        'ramen',
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_goal_item_suggestions(durations, value):
    output = get_goal_item_suggestions(durations, value)
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, tuple)
            vampytest.assert_eq(len(element), 2)
            vampytest.assert_instance(element[0], str)
            vampytest.assert_instance(element[1], str)
    
    return output
