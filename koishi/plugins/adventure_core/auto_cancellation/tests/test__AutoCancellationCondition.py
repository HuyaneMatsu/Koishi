import vampytest

from ..auto_cancellation_condition import AutoCancellationCondition
from ..auto_cancellation_condition_ids import (
    AUTO_CANCELLATION_CONDITION_ID_EQUAL, AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN
)

def _assert_fields_set(auto_cancellation_condition):
    """
    Asserts whether the cancellation condition has all its fields set.
    
    Parameters
    ----------
    auto_cancellation_condition : ``AutoCancellationCondition``
    """
    vampytest.assert_instance(auto_cancellation_condition, AutoCancellationCondition)
    vampytest.assert_instance(auto_cancellation_condition.condition, int)
    vampytest.assert_instance(auto_cancellation_condition.threshold, int)


def test__AutoCancellationCondition__new():
    """
    Tests whether ``AutoCancellationCondition.__new__`` works as intended. 
    """
    condition = AUTO_CANCELLATION_CONDITION_ID_EQUAL
    threshold = 50
    
    auto_cancellation_condition = AutoCancellationCondition(
        condition,
        threshold,
    )
    
    _assert_fields_set(auto_cancellation_condition)
    
    vampytest.assert_eq(auto_cancellation_condition.condition, condition)
    vampytest.assert_eq(auto_cancellation_condition.threshold, threshold)


def test__AutoCancellationCondition__repr():
    """
    Tests whether ``AutoCancellationCondition.__repr__`` works as intended. 
    """
    condition = AUTO_CANCELLATION_CONDITION_ID_EQUAL
    threshold = 50
    
    auto_cancellation_condition = AutoCancellationCondition(
        condition,
        threshold,
    )
    
    output = repr(auto_cancellation_condition)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    condition = AUTO_CANCELLATION_CONDITION_ID_EQUAL
    threshold = 50
    
    
    keyword_parameters = {
        'condition': condition,
        'threshold': threshold,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'condition': AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'threshold': 60,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__AutoCancellationCondition__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``AutoCancellationCondition.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    guild_profile_0 = AutoCancellationCondition(**keyword_parameters_0)
    guild_profile_1 = AutoCancellationCondition(**keyword_parameters_1)
    
    output = guild_profile_0 == guild_profile_1
    vampytest.assert_instance(output, bool)
    return output


def test__AutoCancellationCondition__hash():
    """
    Tests whether ``AutoCancellationCondition.__hash__`` works as intended. 
    """
    condition = AUTO_CANCELLATION_CONDITION_ID_EQUAL
    threshold = 50
    
    auto_cancellation_condition = AutoCancellationCondition(
        condition,
        threshold,
    )
    
    output = hash(auto_cancellation_condition)
    vampytest.assert_instance(output, int)
