import vampytest
from hata import User

from ..base import ConditionBase


def _assert_fields_set(condition):
    """
    Asserts whether the given condition has all of its fields set.
    
    Parameters
    ----------
    condition : ``ConditionBase``
        The instance to check.
    """
    vampytest.assert_instance(condition, ConditionBase)


def test__ConditionBase__new():
    """
    Tests whether ``ConditionBase.__new__`` works as intended.
    """
    condition = ConditionBase()
    _assert_fields_set(condition)


def test__ConditionBase__repr():
    """
    Tests whether ``ConditionBase.__repr__`` works as intended.
    """
    condition = ConditionBase()
    
    output = repr(condition)
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(type(condition).__name__, output)


def test__ConditionBase__hash():
    """
    Tests whether ``ConditionBase.__hash__`` works as intended.
    """
    condition = ConditionBase()
    
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
def test__ConditionBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ConditionBase.__eq__`` works as intended.
    
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
    condition_0 = ConditionBase(**keyword_parameters_0)
    condition_1 = ConditionBase(**keyword_parameters_1)
    
    output = condition_0 == condition_1
    vampytest.assert_instance(output, bool)
    return output


def test__ConditionBase__call__passing():
    """
    Tests whether ``ConditionBase.__call__`` works as intended.
    
    Case: passing.
    """
    condition = ConditionBase()
    user = User.precreate(202412010009, name = 'brain')
    
    output = condition(user)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
