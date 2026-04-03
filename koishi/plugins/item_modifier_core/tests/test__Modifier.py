import vampytest

from ..helpers import construct_modifier_type
from ..modifier import Modifier
from ..modifier_ids import MODIFIER_ID__STAT_HOUSEWIFE
from ..modifier_kinds import MODIFIER_KIND__PERCENT


def _assert_fields_set(modifier):
    """
    Asserts whether the given modifier has all of its fields set.
    
    Parameters
    ----------
    modifier : ``Modifier``
        The modifier to test.
    """
    vampytest.assert_instance(modifier, Modifier)
    vampytest.assert_instance(modifier.amount, int)
    vampytest.assert_instance(modifier.type, int)


def test__Modifier__new():
    """
    Tests whether ``Modifier.__new__`` works as intended.
    """
    modifier_type = construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__PERCENT)
    amount = 4
    
    modifier = Modifier(modifier_type, amount)
    _assert_fields_set(modifier)
    
    vampytest.assert_eq(modifier.amount, amount)
    vampytest.assert_eq(modifier.type, modifier_type)


def test__Modifier__repr():
    """
    Tests whether ``Modifier.__repr__`` works as intended.
    """
    modifier_type = construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__PERCENT)
    amount = 4
    
    modifier = Modifier(modifier_type, amount)
    
    output = repr(modifier)
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(type(modifier).__name__, output)
    vampytest.assert_in(str(4), output)
    vampytest.assert_in('%', output)
    vampytest.assert_in('Housewife', output)
