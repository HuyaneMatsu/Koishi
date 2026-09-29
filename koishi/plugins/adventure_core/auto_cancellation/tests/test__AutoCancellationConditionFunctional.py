from types import FunctionType

import vampytest

from ..auto_cancellation_condition_functional import (
    AutoCancellationConditionFunctional, auto_cancellation_condition_functional_create
)


def test__auto_cancellation_condition_functional_create():
    name = 'orin'
    function = lambda value : True
    
    auto_cancellation_condition_functional = auto_cancellation_condition_functional_create(
        name,
        function,
    )
    
    vampytest.assert_instance(auto_cancellation_condition_functional, AutoCancellationConditionFunctional)
    vampytest.assert_instance(auto_cancellation_condition_functional.name, str)
    vampytest.assert_instance(auto_cancellation_condition_functional.function, FunctionType)
    
    vampytest.assert_eq(auto_cancellation_condition_functional.name, name)
    vampytest.assert_eq(auto_cancellation_condition_functional.function, function)
