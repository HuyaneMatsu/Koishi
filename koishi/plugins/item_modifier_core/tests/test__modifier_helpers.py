import vampytest

from ..helpers import construct_modifier_type, get_modifier_name_and_amount_postfix
from ..modifier_kinds import MODIFIER_KIND__FLAT, MODIFIER_KIND__PERCENT


def test__modifier_type_operations():
    """
    Tests whether ``construct_modifier_type`` and ``get_modifier_name_and_amount_postfix`` works as intended.
    """
    modifier_type = 5
    
    modifier_names = {
        modifier_type: 'pudding'
    }
    
    mocked_get_modifier_name_and_amount_postfix = vampytest.mock_globals(
        get_modifier_name_and_amount_postfix,
        MODIFIER_ID_NAMES = modifier_names,
    )
    
    stat_type_flat = construct_modifier_type(modifier_type, MODIFIER_KIND__FLAT)
    vampytest.assert_instance(stat_type_flat, int)
    vampytest.assert_eq(mocked_get_modifier_name_and_amount_postfix(stat_type_flat), ('pudding', None))
    
    stat_type_percent = construct_modifier_type(modifier_type, MODIFIER_KIND__PERCENT)
    vampytest.assert_instance(stat_type_percent, int)
    vampytest.assert_eq(mocked_get_modifier_name_and_amount_postfix(stat_type_percent), ('pudding', '%'))
