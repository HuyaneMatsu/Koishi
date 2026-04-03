from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import User

from ..weekend import ConditionWeekend


def _assert_fields_set(condition):
    """
    Asserts whether the given condition has all of its fields set.
    
    Parameters
    ----------
    condition : ``ConditionWeekend``
        The instance to check.
    """
    vampytest.assert_instance(condition, ConditionWeekend)


def test__ConditionWeekend__new():
    """
    Tests whether ``ConditionWeekend.__new__`` works as intended.
    """
    condition = ConditionWeekend()
    _assert_fields_set(condition)


def test__ConditionWeekend__repr():
    """
    Tests whether ``ConditionWeekend.__repr__`` works as intended.
    """
    condition = ConditionWeekend()
    
    output = repr(condition)
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(type(condition).__name__, output)


def test__ConditionWeekend__hash():
    """
    Tests whether ``ConditionWeekend.__hash__`` works as intended.
    """
    condition = ConditionWeekend()
    
    output = hash(condition)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    keyword_parameters = {}
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    
@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ConditionWeekend__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ConditionWeekend.__eq__`` works as intended.
    
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
    condition_0 = ConditionWeekend(**keyword_parameters_0)
    condition_1 = ConditionWeekend(**keyword_parameters_1)
    
    output = condition_0 == condition_1
    vampytest.assert_instance(output, bool)
    return output


def test__ConditionWeekend__call__passing():
    """
    Tests whether ``ConditionWeekend.__call__`` works as intended.
    
    Case: passing.
    """
    condition = ConditionWeekend()
    user = User.precreate(202412010020, name = 'brain')
    
    class DateTimeMock:
        def now(*a, **k):
            return DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
        
    
    mocked = vampytest.mock_globals(
        type(condition).__call__,
        DateTime = DateTimeMock
    )
    
    output = mocked(condition, user)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__ConditionWeekend__call__failing():
    """
    Tests whether ``ConditionWeekend.__call__`` works as intended.
    
    Case: failing.
    """
    condition = ConditionWeekend()
    user = User.precreate(202412010021, name = 'brain')
    
    class DateTimeMock:
        def now(*a, **k):
            return DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
        
    
    mocked = vampytest.mock_globals(
        type(condition).__call__,
        DateTime = DateTimeMock
    )
    
    output = mocked(condition, user)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
