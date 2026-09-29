import vampytest

from ..auto_cancellation_condition import AutoCancellationCondition, auto_cancellation_condition_create
from ..auto_cancellation_condition_ids import AUTO_CANCELLATION_CONDITION_ID_EQUAL


def test__auto_cancellation_condition_create():
    condition = AUTO_CANCELLATION_CONDITION_ID_EQUAL
    threshold = 50
    
    auto_cancellation_condition = auto_cancellation_condition_create(
        condition,
        threshold,
    )
    
    vampytest.assert_instance(auto_cancellation_condition, AutoCancellationCondition)
    vampytest.assert_instance(auto_cancellation_condition.condition, int)
    vampytest.assert_instance(auto_cancellation_condition.threshold, int)
    
    vampytest.assert_eq(auto_cancellation_condition.condition, condition)
    vampytest.assert_eq(auto_cancellation_condition.threshold, threshold)
