import vampytest
from hata import BUILTIN_EMOJIS

from ...item_core import ITEM_FLAG_EDIBLE, Item

from ..helpers import construct_modifier_type
from ..modifier import Modifier
from ..modifier_ids import MODIFIER_ID__FISHING
from ..modifier_kinds import MODIFIER_KIND__FLAT, MODIFIER_KIND__PERCENT
from ..utils import accumulate_modifier_values


def test__accumulate_modifier_values():
    """
    Tests whether ``accumulate_modifier_values`` works as intended.
    """
    modifier_0 = Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT), 20)
    modifier_1 = Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__PERCENT), 10)
    
    item_0 = Item(
        9999,
        'pudding',
        BUILTIN_EMOJIS['cat'],
        'yummy',
        ITEM_FLAG_EDIBLE,
        1,
        1,
        (
            modifier_0,
            modifier_1,
        ),
    )
    
    item_1 = Item(
        9998,
        'pudding',
        BUILTIN_EMOJIS['cat'],
        'yummy',
        ITEM_FLAG_EDIBLE,
        1,
        1,
        (
            modifier_0,
        ),
    )
    
    output = accumulate_modifier_values(None, item_0, item_1, None)
    
    vampytest.assert_instance(output, dict)
    vampytest.assert_eq(
        output,
        {
            construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT) : 40,
            construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__PERCENT) : 10,
        },
    )
