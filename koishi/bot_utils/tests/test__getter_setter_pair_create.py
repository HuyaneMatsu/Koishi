from types import FunctionType

import vampytest

from ..getter_setter_pair import getter_setter_pair_create


def test__getter_setter_pair_create():
    """
    Tests whether ``getter_setter_pair_create`` works as intended.
    """
    getter, setter = getter_setter_pair_create()
    vampytest.assert_instance(getter, FunctionType)
    vampytest.assert_instance(setter, FunctionType)
    
    output = getter()
    vampytest.assert_is(output, None)
    
    value = object()
    setter(value)
    output = getter()
    vampytest.assert_is(output, value)
