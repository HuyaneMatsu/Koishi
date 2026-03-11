import vampytest

from ..constants import ITEM_GROUPS
from ..item_group import ItemGroup
from ..item_group_ids import ITEM_GROUP_ID_KNIFE
from ..utils import get_item_group_nullable


def test__get_item_group_nullable__existing():
    """
    Tests whether ``get_item_group_nullable`` works as intended.
    
    Case: existing.
    """
    item_group_id = ITEM_GROUP_ID_KNIFE
    
    length_before = len(ITEM_GROUPS)
    
    output = get_item_group_nullable(item_group_id)
    vampytest.assert_instance(output, ItemGroup)
    vampytest.assert_eq(output.id, item_group_id)
    
    length_after = len(ITEM_GROUPS)
    
    vampytest.assert_eq(length_before, length_after)


def test__get_item_group_nullable__missing():
    """
    Tests whether ``get_item_group_nullable`` works as intended.
    
    Case: missing.
    """
    item_group_id = 999999
    
    length_before = len(ITEM_GROUPS)
    
    output = get_item_group_nullable(item_group_id)
    vampytest.assert_is(output, None)
    
    length_after = len(ITEM_GROUPS)
    
    vampytest.assert_eq(length_before, length_after)


def test__get_item_group_nullable__zero():
    """
    Tests whether ``get_item_group_nullable`` works as intended.
    
    Case: zero.
    """
    item_group_id = 0
    
    length_before = len(ITEM_GROUPS)
    
    output = get_item_group_nullable(item_group_id)
    vampytest.assert_is(output, None)
    
    length_after = len(ITEM_GROUPS)
    
    vampytest.assert_eq(length_before, length_after)
