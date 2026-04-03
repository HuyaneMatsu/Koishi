import vampytest

from ....bot_utils.models import DB_ENGINE

from ...item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY, get_item

from ..constants import INVENTORIES, INVENTORY_CACHE
from ..inventory import Inventory
from ..queries import save_inventory


async def test__save_inventory__nothing_to_save():
    """
    Tests whether ``save_inventory`` works as intended.
    
    Case: nothing to save.
    
    This function is a coroutine.
    """
    async def mock_query_save_inventory(input_user_id):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        save_inventory,
        query_save_inventory = mock_query_save_inventory,
    )
    
    user_id = 202503290010
    inventory = Inventory(user_id)
    
    try:
        await mocked(inventory)
    finally:
        INVENTORY_CACHE.clear()
        INVENTORIES.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__save_inventory__things_to_save():
    """
    Tests whether ``save_inventory`` works as intended.
    
    Case: things to save.
    
    This function is a coroutine.
    """
    user_id = 202503290011
    
    inventory = Inventory(user_id)
    inventory.modify_item_amount(get_item(ITEM_ID_STRAWBERRY), 5)
    inventory.modify_item_amount(get_item(ITEM_ID_PEACH), 4)
    
    try:
        await save_inventory(inventory)
        
        vampytest.assert_is_not(inventory.item_entries, None)
        vampytest.assert_eq(inventory.item_entries.keys(), {ITEM_ID_STRAWBERRY, ITEM_ID_PEACH})
        vampytest.assert_eq(inventory.item_entries[ITEM_ID_STRAWBERRY].amount, 5)
        vampytest.assert_eq(inventory.item_entries[ITEM_ID_PEACH].amount, 4)
        
        vampytest.assert_is(inventory.item_entries_modified, None)
    finally:
        INVENTORY_CACHE.clear()
        INVENTORIES.clear()
