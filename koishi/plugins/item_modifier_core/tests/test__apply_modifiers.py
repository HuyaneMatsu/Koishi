import vampytest


from ..helpers import construct_modifier_type
from ..modifier_ids import MODIFIER_ID__FISHING
from ..modifier_kinds import MODIFIER_KIND__FLAT, MODIFIER_KIND__PERCENT
from ..utils import apply_modifiers


def test__apply_modifiers():
    """
    Tests whether ``apply_modifiers`` works as intended.
    """
    accumulated_modifiers = {
        construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT) : 40,
        construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__PERCENT) : 10,
    }
    
    output = apply_modifiers(10, accumulated_modifiers, MODIFIER_ID__FISHING)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 55)
