import vampytest

from ..constants import ITEMS
from ..item import Item
from ..item_ids import ITEM_ID_PEACH
from ..utils import get_item


def test__get_item__existing():
    """
    Tests whether ``get_item`` works as intended.
    
    Case: existing.
    """
    item_id = ITEM_ID_PEACH
    
    length_before = len(ITEMS)
    
    output = get_item(item_id)
    vampytest.assert_instance(output, Item)
    vampytest.assert_eq(output.id, item_id)
    
    
    length_after = len(ITEMS)
    
    vampytest.assert_eq(length_before, length_after)


def test__get_item__new():
    """
    Tests whether ``get_item`` works as intended.
    
    Case: new.
    """
    item_id = 999999
    try:
        length_before = len(ITEMS)
        
        output = get_item(item_id)
        vampytest.assert_instance(output, Item)
        vampytest.assert_eq(output.id, item_id)
        vampytest.assert_is(ITEMS.get(item_id, None), output)
        
        
        length_after = len(ITEMS)
        
        vampytest.assert_ne(length_before, length_after)
    
    finally:
        try:
            del ITEMS[item_id]
        except KeyError:
            pass
