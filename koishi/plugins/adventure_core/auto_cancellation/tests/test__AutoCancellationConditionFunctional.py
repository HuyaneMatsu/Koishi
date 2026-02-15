from types import FunctionType

import vampytest

from ..auto_cancellation_condition_functional import AutoCancellationConditionFunctional


def _assert_fields_set(auto_cancellation_condition_functional):
    """
    Asserts whether the cancellation name has all its fields set.
    
    Parameters
    ----------
    auto_cancellation_condition_functional : ``AutoCancellationConditionFunctional``
    """
    vampytest.assert_instance(auto_cancellation_condition_functional, AutoCancellationConditionFunctional)
    vampytest.assert_instance(auto_cancellation_condition_functional.name, str)
    vampytest.assert_instance(auto_cancellation_condition_functional.function, FunctionType)


def test__AutoCancellationConditionFunctional__new():
    """
    Tests whether ``AutoCancellationConditionFunctional.__new__`` works as intended. 
    """
    name = 'orin'
    function = lambda value : True
    
    auto_cancellation_condition_functional = AutoCancellationConditionFunctional(
        name,
        function,
    )
    
    _assert_fields_set(auto_cancellation_condition_functional)
    
    vampytest.assert_eq(auto_cancellation_condition_functional.name, name)
    vampytest.assert_eq(auto_cancellation_condition_functional.function, function)


def test__AutoCancellationConditionFunctional__repr():
    """
    Tests whether ``AutoCancellationConditionFunctional.__repr__`` works as intended. 
    """
    name = 'orin'
    function = lambda value : True
    
    auto_cancellation_condition_functional = AutoCancellationConditionFunctional(
        name,
        function,
    )
    
    output = repr(auto_cancellation_condition_functional)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    name = 'orin'
    function = lambda value : True
    
    
    keyword_parameters = {
        'name' : name,
        'function' : function,
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
            'name' : 'okuu',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'function' : lambda value : False,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__AutoCancellationConditionFunctional__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``AutoCancellationConditionFunctional.__eq__`` works as intended.
    
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
    guild_profile_0 = AutoCancellationConditionFunctional(**keyword_parameters_0)
    guild_profile_1 = AutoCancellationConditionFunctional(**keyword_parameters_1)
    
    output = guild_profile_0 == guild_profile_1
    vampytest.assert_instance(output, bool)
    return output


def test__AutoCancellationConditionFunctional__hash():
    """
    Tests whether ``AutoCancellationConditionFunctional.__hash__`` works as intended. 
    """
    name = 'orin'
    function = lambda value : True
    
    auto_cancellation_condition_functional = AutoCancellationConditionFunctional(
        name,
        function,
    )
    
    output = hash(auto_cancellation_condition_functional)
    vampytest.assert_instance(output, int)
