import vampytest

from ....unit_core import AMOUNT_TYPE_COUNT

from ..goal import GOAL_TYPE_ITEM_EXACT, goal_create_item_exact
from ..serialisation import goal_serialise


def test__goal_serialise():
    item_id = 5
    amount_type = AMOUNT_TYPE_COUNT
    amount_required = 12
    
    goal = goal_create_item_exact(
        item_id,
        amount_type,
        amount_required,
    )
    
    output = goal_serialise(goal)
    vampytest.assert_instance(output, bytes)
    vampytest.assert_eq(
        output,
        b''.join([
            GOAL_TYPE_ITEM_EXACT.to_bytes(1, 'little'),
            item_id.to_bytes(4, 'little'),
            amount_type.to_bytes(1, 'little'),
            amount_required.to_bytes(8, 'little'),
        ]),
    )
