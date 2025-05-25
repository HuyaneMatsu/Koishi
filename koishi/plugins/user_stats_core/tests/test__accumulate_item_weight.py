import vampytest
from hata import BUILTIN_EMOJIS

from ...item_core import ITEM_FLAG_EDIBLE, Item

from ..calculations import accumulate_item_weight


def test__accumulate_item_weight():
    """
    Tests whether ``accumulate_item_weight`` works as intended.
    """
    item_0 = Item(
        9999,
        'pudding',
        BUILTIN_EMOJIS['cat'],
        'yummy',
        ITEM_FLAG_EDIBLE,
        1,
        1000,
        None
    )
    
    item_1 = Item(
        9998,
        'pudding',
        BUILTIN_EMOJIS['cat'],
        'yummy',
        ITEM_FLAG_EDIBLE,
        1,
        300,
        None,
    )
    
    output = accumulate_item_weight(None, item_0, item_1, None)
    
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1300)
