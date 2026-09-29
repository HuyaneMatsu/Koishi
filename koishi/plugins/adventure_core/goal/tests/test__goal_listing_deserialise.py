import vampytest

from ....unit_core import AMOUNT_TYPE_COUNT

from ..goal import GOAL_TYPE_ITEM_EXACT, Goal
from ..serialisation import goal_listing_deserialise


def test__goal_deserialise():
    item_id = 5
    amount_type = AMOUNT_TYPE_COUNT
    amount_required_0 = 12
    amount_required_1 = 13
    
    data = b''.join([
        GOAL_TYPE_ITEM_EXACT.to_bytes(1, 'little'),
        item_id.to_bytes(4, 'little'),
        amount_type.to_bytes(1, 'little'),
        amount_required_0.to_bytes(8, 'little'),
        
        GOAL_TYPE_ITEM_EXACT.to_bytes(1, 'little'),
        item_id.to_bytes(4, 'little'),
        amount_type.to_bytes(1, 'little'),
        amount_required_1.to_bytes(8, 'little'),
    ])
    
    goal_listing = goal_listing_deserialise(data)
    
    vampytest.assert_instance(goal_listing, list, nullable = True)
    vampytest.assert_is_not(goal_listing, None)
    vampytest.assert_eq(len(goal_listing), 2)
    
    goal = goal_listing[0]
    vampytest.assert_instance(goal, Goal)
    vampytest.assert_eq(goal.behaviour.type, GOAL_TYPE_ITEM_EXACT)
    vampytest.assert_eq(goal.configuration.item_id, item_id)
    vampytest.assert_eq(goal.configuration.amount_type, amount_type)
    vampytest.assert_eq(goal.configuration.amount_required, amount_required_0)
    
    goal = goal_listing[1]
    vampytest.assert_instance(goal, Goal)
    vampytest.assert_eq(goal.behaviour.type, GOAL_TYPE_ITEM_EXACT)
    vampytest.assert_eq(goal.configuration.item_id, item_id)
    vampytest.assert_eq(goal.configuration.amount_type, amount_type)
    vampytest.assert_eq(goal.configuration.amount_required, amount_required_1)
