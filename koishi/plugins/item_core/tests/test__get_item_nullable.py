import vampytest

from ..constants import ITEMS
from ..item import Item
from ..item_ids import ITEM_ID_PEACH
from ..utils import get_item_nullable


def test__get_item_nullable__existing():
    """
    Tests whether ``get_item_nullable`` works as intended.
    
    Case: existing.
    """
    item_id = ITEM_ID_PEACH
    
    length_before = len(ITEMS)
    
    output = get_item_nullable(item_id)
    vampytest.assert_instance(output, Item)
    vampytest.assert_eq(output.id, item_id)
    
    length_after = len(ITEMS)
    
    vampytest.assert_eq(length_before, length_after)


def test__get_item_nullable__missing():
    """
    Tests whether ``get_item_nullable`` works as intended.
    
    Case: missing.
    """
    item_id = 999999
    
    length_before = len(ITEMS)
    
    output = get_item_nullable(item_id)
    vampytest.assert_is(output, None)
    
    length_after = len(ITEMS)
    
    vampytest.assert_eq(length_before, length_after)


def test__get_item_nullable__zero():
    """
    Tests whether ``get_item_nullable`` works as intended.
    
    Case: zero.
    """
    item_id = 0
    
    length_before = len(ITEMS)
    
    output = get_item_nullable(item_id)
    vampytest.assert_is(output, None)
    
    length_after = len(ITEMS)
    
    vampytest.assert_eq(length_before, length_after)
