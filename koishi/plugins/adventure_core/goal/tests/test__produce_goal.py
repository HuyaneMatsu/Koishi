import vampytest

from .....bot_utils.constants import EMOJI__HEART_CURRENCY

from ....item_core import ITEM_ID_PEACH, get_item_nullable
from ....unit_core import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT

from ..goal import goal_create_default, goal_create_item_exact
from ..utils import produce_goal


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    yield (
        goal_create_default(),
        '\*none\*',
    )
    
    yield (
        goal_create_item_exact(item_peach.id, AMOUNT_TYPE_COUNT, 2000),
        f'2000 {item_peach.emoji} {item_peach.name}'
    )
    
    yield (
        goal_create_item_exact(item_peach.id, AMOUNT_TYPE_WEIGHT, 2000),
        f'2 kg {item_peach.emoji} {item_peach.name}'
    )
    
    yield (
        goal_create_item_exact(item_peach.id, AMOUNT_TYPE_VALUE, 2000),
        f'2000 {EMOJI__HEART_CURRENCY} worth of {item_peach.emoji} {item_peach.name}'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_goal(goal):
    parts = [*produce_goal(goal)]
    
    for part in parts:
        vampytest.assert_instance(part, str)
    
    return ''.join(parts)
