import vampytest
from hata import User

from ..name import ConditionName


def _assert_fields_set(condition):
    """
    Asserts whether the given condition has all of its fields set.
    
    Parameters
    ----------
    condition : ``ConditionName``
        The instance to check.
    """
    vampytest.assert_instance(condition, ConditionName)
    vampytest.assert_instance(condition.name, str)


def test__ConditionName__new():
    """
    Tests whether ``ConditionName.__new__`` works as intended.
    """
    name = 'brain'
    
    condition = ConditionName(name)
    _assert_fields_set(condition)
    
    vampytest.assert_is(condition.name, name)


def test__ConditionName__repr():
    """
    Tests whether ``ConditionName.__repr__`` works as intended.
    """
    name = 'brain'
    
    condition = ConditionName(name)
    
    output = repr(condition)
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(type(condition).__name__, output)
    vampytest.assert_in(f' name = {name!r}', output)


def test__ConditionName__hash():
    """
    Tests whether ``ConditionName.__hash__`` works as intended.
    """
    name = 'brain'
    
    condition = ConditionName(name)
    
    output = hash(condition)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    name = 'brain'
    
    keyword_parameters = {
        'name': name,
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
            'name': 'beloved',
        },
        False,
    )
    
    
@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ConditionName__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ConditionName.__eq__`` works as intended.
    
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
    condition_0 = ConditionName(**keyword_parameters_0)
    condition_1 = ConditionName(**keyword_parameters_1)
    
    output = condition_0 == condition_1
    vampytest.assert_instance(output, bool)
    return output


def test__ConditionName__call__passing():
    """
    Tests whether ``ConditionName.__call__`` works as intended.
    
    Case: passing.
    """
    name = 'brain'
    user = User.precreate(202412010030, name = 'brain')
    condition = ConditionName(name)
    
    output = condition(user)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__ConditionName__call__failing():
    """
    Tests whether ``ConditionName.__call__`` works as intended.
    
    Case: failing.
    """
    name = 'brain'
    condition = ConditionName(name)
    user = User.precreate(202412010031, name = 'beloved')
    
    output = condition(user)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
