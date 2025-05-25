__all__ = ('get_inventory', 'save_inventory')

from functools import partial as partial_func

from scarletio import Future, Task, copy_docs, get_event_loop

from ...bot_utils.models import DB_ENGINE, item_model, ITEM_TABLE

from .constants import (
    INVENTORIES, INVENTORY_CACHE, INVENTORY_CACHE_SIZE_MAX, INVENTORY_GET_TASKS, INVENTORY_SAVE_TASKS
)
from .inventory import Inventory


EVENT_LOOP = get_event_loop()


def _inventory_query_done_callback(key, waiters, task):
    """
    Added as a callback of a query to set the result into the waiters and caches the result.
    
    Parameters
    ----------
    key : `int`
        The user's identifier used as a key.
    
    waiters : `list<Future>`
        Result waiters.
    
    task : ``Future``
        The ran task.
    """
    try:
        inventory = task.get_result()
    except BaseException as exception:
        for waiter in waiters:
            waiter.set_exception_if_pending(exception)
    else:
        INVENTORIES[key] = inventory
        INVENTORY_CACHE[key] = inventory
        if len(INVENTORY_CACHE) > INVENTORY_CACHE_SIZE_MAX:
            del INVENTORY_CACHE[next(iter(INVENTORY_CACHE))]
        
        for waiter in waiters:
            waiter.set_result_if_pending(inventory)
        
    finally:
        del INVENTORY_GET_TASKS[key]


async def get_inventory(user_id):
    """
    Gets the user's inventory.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    inventory : ``Inventory``
    """
    try:
        inventory = INVENTORY_CACHE[user_id]
    except KeyError:
        pass
    else:
        INVENTORY_CACHE.move_to_end(user_id)
        return inventory
    
    try:
        inventory = INVENTORIES[user_id]
    except KeyError:
        pass
    else:
        INVENTORY_CACHE[user_id] = inventory
        if len(INVENTORY_CACHE) > INVENTORY_CACHE_SIZE_MAX:
            del INVENTORY_CACHE[next(iter(INVENTORY_CACHE))]
        return inventory
    
    try:
        task, waiters = INVENTORY_GET_TASKS[user_id]
    except KeyError:
        waiters = []
        task = Task(EVENT_LOOP, query_inventory(user_id))
        task.add_done_callback(partial_func(_inventory_query_done_callback, user_id, waiters))
        INVENTORY_GET_TASKS[user_id] = (task, waiters)
    
    waiter = Future(EVENT_LOOP)
    waiters.append(waiter)
    return await waiter


def _inventory_save_done_callback(key, waiters, task):
    """
    Added as a callback to a save query to set the result of it into its waiters.
    
    Parameters
    ----------
    key : `int`
        The user's identifier used as a key.
    
    waiters : `list<Future>`
        Result waiters.
    
    task : ``Future``
        The ran task.
    """
    try:
        inventory = task.get_result()
    except BaseException as exception:
        for waiter in waiters:
            waiter.set_exception_if_pending(exception)
    else:
        for waiter in waiters:
            waiter.set_result_if_pending(inventory)
        
    finally:
        del INVENTORY_SAVE_TASKS[key]
    

async def save_inventory(inventory):
    """
    Saves the modifications done to the inventory.
    
    This function is a coroutine.
    
    Parameters
    ----------
    inventory : ``Inventory``
        The inventory to save.
    """
    if inventory.item_entries_modified is None:
        return
    
    user_id = inventory.user_id
    
    try:
        task, waiters = INVENTORY_SAVE_TASKS[user_id]
    except KeyError:
        waiters = []
        task = Task(EVENT_LOOP, query_save_inventory(inventory))
        task.add_done_callback(partial_func(_inventory_save_done_callback, user_id, waiters))
        INVENTORY_SAVE_TASKS[user_id] = (task, waiters)
    
    waiter = Future(EVENT_LOOP)
    waiters.append(waiter)
    return await waiter


async def query_inventory(user_id):
    """
    Queries the inventory for the given user identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    Returns
    -------
    inventory : ``Inventory``
    """
    async with DB_ENGINE.connect() as connector:
        results = await connector.execute(
            ITEM_TABLE.select().where(
                item_model.user_id == user_id,
            )
        )
    
        entries = await results.fetchall()
        return Inventory.from_entries(user_id, entries)


if (DB_ENGINE is None):
    @copy_docs(query_inventory)
    async def query_inventory(user_id):
        return Inventory(user_id)


async def query_save_inventory(inventory):
    """
    Saves the modifications of the given inventory.
    
    This function is a coroutine.
    
    Parameters
    ----------
    inventory : ``Inventory``
        The inventory to save.
    """
    async with DB_ENGINE.connect() as connector:
        while True:
            item_entry = inventory.get_modified_item_entry()
            if (item_entry is None):
                break
            
            amount = item_entry.amount
            entry_id = item_entry.entry_id
            
            # New but instantly deleted?
            if (entry_id == -1) and (not amount):
                pass
            
            # New?
            elif (entry_id == -1):
                response = await connector.execute(
                    ITEM_TABLE.insert().values(
                        user_id = inventory.user_id,
                        amount = amount,
                        item_id = item_entry.item.id,
                    ).returning(    
                        item_model.id,
                    )
                )
                
                # Update `.entry_id`
                entry = await response.fetchone()
                item_entry.entry_id = entry[0]
            
            # Deleted?
            elif (not amount):
                await connector.execute(
                    ITEM_TABLE.delete().where(
                        item_model.id == entry_id
                    )
                )
            
            # Updated?
            else:
                await connector.execute(
                    ITEM_TABLE.update(
                        item_model.id == entry_id
                    ).values(
                        amount = amount,
                    )
                )
            
            inventory.apply_modified_item_entry(item_entry)
            continue


if (DB_ENGINE is None):
    @copy_docs(query_save_inventory)
    async def query_save_inventory(inventory):
        while True:
            item_entry = inventory.get_modified_item_entry()
            if (item_entry is None):
                break
            
            inventory.apply_modified_item_entry(item_entry)
            continue
