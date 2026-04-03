import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ..constants import INVENTORIES, INVENTORY_CACHE, INVENTORY_GET_TASKS
from ..inventory import Inventory
from ..queries import get_inventory


async def test__get_inventory__in_cache():
    """
    Tests whether ``get_inventory`` works as intended.
    
    Case: in cache.
    
    This function is a coroutine.
    """
    async def mock_query_inventory(input_user_id):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_inventory,
        query_inventory = mock_query_inventory,
    )
    
    user_id_0 = 202503290000
    user_id_1 = 202503290001
    
    inventory_0 = Inventory(user_id_0)
    inventory_1 = Inventory(user_id_1)
    
    try:
        INVENTORY_CACHE[user_id_0] = inventory_0
        INVENTORY_CACHE[user_id_1] = inventory_1
        INVENTORIES[user_id_0] = inventory_0
        INVENTORIES[user_id_1] = inventory_1
        
        output = await mocked(user_id_0)
        
        vampytest.assert_instance(output, Inventory)
        vampytest.assert_eq(output, inventory_0)
        
        vampytest.assert_eq(
            [*INVENTORY_CACHE.items()],
            [
                (user_id_1, inventory_1),
                (user_id_0, inventory_0),
            ],
        )
        vampytest.assert_eq(
            {key: value for key, value in INVENTORIES.items()},
            {
                user_id_0 : inventory_0,
                user_id_1 : inventory_1,
            },
        )
    finally:
        INVENTORY_CACHE.clear()
        INVENTORIES.clear()


async def test__get_inventory__in_weak_cache():
    """
    Tests whether ``get_inventory`` works as intended.
    
    Case: in weak cache.
    
    This function is a coroutine.
    """
    async def mock_query_inventory(input_user_id):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_inventory,
        query_inventory = mock_query_inventory,
    )
    
    user_id = 202503290004
    
    inventory = Inventory(user_id)
    
    try:
        INVENTORIES[user_id] = inventory
        
        output = await mocked(user_id)
        
        vampytest.assert_instance(output, Inventory)
        vampytest.assert_eq(output, inventory)
        
        vampytest.assert_eq(
            [*INVENTORY_CACHE.items()],
            [
                (user_id, inventory),
            ],
        )
        vampytest.assert_eq(
            {key: value for key, value in INVENTORIES.items()},
            {
                user_id : inventory,
            },
        )
    finally:
        INVENTORY_CACHE.clear()
        INVENTORIES.clear()


async def test__get_inventory__query():
    """
    Tests whether ``get_inventory`` works as intended.
    
    Case: query.
    
    This function is a coroutine.
    """
    async def mock_query_inventory(input_user_id):
        nonlocal user_id
        nonlocal inventory
        
        vampytest.assert_eq(input_user_id, user_id)
        
        return inventory
    
    
    mocked = vampytest.mock_globals(
        get_inventory,
        query_inventory = mock_query_inventory,
    )
    
    user_id = 202503290002
    
    inventory = Inventory(user_id)
    
    try:
        output = await mocked(user_id)
        
        vampytest.assert_instance(output, Inventory)
        vampytest.assert_eq(output, inventory)
        
        vampytest.assert_eq(
            [*INVENTORY_CACHE.items()],
            [
                (user_id, inventory),
            ],
        )
        vampytest.assert_eq(
            {key: value for key, value in INVENTORIES.items()},
            {
                user_id : inventory,
            },
        )
    finally:
        INVENTORY_CACHE.clear()
        INVENTORIES.clear()


async def test__get_inventory__double_query():
    """
    Tests whether ``get_inventory`` works as intended.
    
    Case: double query.
    
    This function is a coroutine.
    """
    async def mock_query_inventory(input_user_id):
        nonlocal user_id
        nonlocal inventory
        
        await skip_ready_cycle()
        vampytest.assert_eq(input_user_id, user_id)
        
        return inventory
    
    
    mocked = vampytest.mock_globals(
        get_inventory,
        query_inventory = mock_query_inventory,
    )
    
    user_id = 202503290003
    
    inventory = Inventory(user_id)
    
    event_loop = get_event_loop()
    
    try:
        task_0 = Task(event_loop, mocked(user_id))
        task_1 = Task(event_loop, mocked(user_id))
        
        await skip_ready_cycle()
        vampytest.assert_eq(len(INVENTORY_GET_TASKS), 1)
        
        output_0 = await task_0
        output_1 = await task_1
        
        vampytest.assert_is(output_0, output_1)
        
        vampytest.assert_instance(output_0, Inventory)
        vampytest.assert_eq(output_0, inventory)
        
        vampytest.assert_eq(
            [*INVENTORY_CACHE.items()],
            [
                (user_id, inventory),
            ],
        )
        vampytest.assert_eq(
            {key: value for key, value in INVENTORIES.items()},
            {
                user_id : inventory,
            },
        )
        
        vampytest.assert_eq(len(INVENTORY_GET_TASKS), 0)
        
    finally:
        INVENTORY_CACHE.clear()
        INVENTORIES.clear()
