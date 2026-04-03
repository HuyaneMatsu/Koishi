import vampytest

from ..constants import ITEM_GROUPS
from ..item_group import ItemGroup
from ..item_group_ids import ITEM_GROUP_ID_KNIFE
from ..utils import get_item_group


def test__get_item_group__existing():
    """
    Tests whether ``get_item_group`` works as intended.
    
    Case: existing.
    """
    item_group_id = ITEM_GROUP_ID_KNIFE
    
    length_before = len(ITEM_GROUPS)
    
    output = get_item_group(item_group_id)
    vampytest.assert_instance(output, ItemGroup)
    vampytest.assert_eq(output.id, item_group_id)
    
    
    length_after = len(ITEM_GROUPS)
    
    vampytest.assert_eq(length_before, length_after)


def test__get_item_group__new():
    """
    Tests whether ``get_item_group`` works as intended.
    
    Case: new.
    """
    item_group_id = 999999
    try:
        length_before = len(ITEM_GROUPS)
        
        output = get_item_group(item_group_id)
        vampytest.assert_instance(output, ItemGroup)
        vampytest.assert_eq(output.id, item_group_id)
        vampytest.assert_is(ITEM_GROUPS.get(item_group_id, None), output)
        
        
        length_after = len(ITEM_GROUPS)
        
        vampytest.assert_ne(length_before, length_after)
    
    finally:
        try:
            del ITEM_GROUPS[item_group_id]
        except KeyError:
            pass
