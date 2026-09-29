import vampytest

from ....unit_core import AMOUNT_TYPE_COUNT

from ..goal import GOAL_TYPE_ITEM_EXACT, Goal
from ..serialisation import goal_deserialise


def test__goal_deserialise():
    item_id = 5
    amount_type = AMOUNT_TYPE_COUNT
    amount_required = 12
    
    data = b''.join([
        GOAL_TYPE_ITEM_EXACT.to_bytes(1, 'little'),
        item_id.to_bytes(4, 'little'),
        amount_type.to_bytes(1, 'little'),
        amount_required.to_bytes(8, 'little'),
    ])
    
    goal = goal_deserialise(data)
    
    vampytest.assert_instance(goal, Goal, nullable = True)
    vampytest.assert_is_not(goal, None)
    
    vampytest.assert_eq(goal.behaviour.type, GOAL_TYPE_ITEM_EXACT)
    vampytest.assert_eq(goal.configuration.item_id, item_id)
    vampytest.assert_eq(goal.configuration.amount_type, amount_type)
    vampytest.assert_eq(goal.configuration.amount_required, amount_required)
