__all__ = (
    'adventure_get_active', 'adventure_listing_get_active', 'adventure_get', 'adventure_listing_get_page', 'adventure_save'
)

from functools import partial as partial_func
from itertools import count

from scarletio import Future, Task, copy_docs, get_event_loop
from sqlalchemy import func as alchemy_function
from sqlalchemy.sql import asc, select

from ...bot_utils.models import ADVENTURE_TABLE, DB_ENGINE, adventure_model

from .adventure import (
    ADVENTURE_STATE_FINALISED, adventure_action_listing_serialise, adventure_collect_modifications,
    adventure_create_from_entry
)
from .constants import (
    ADVENTURES, ADVENTURES_ACTIVE, ADVENTURE_CACHE, ADVENTURE_CACHE_SIZE_MAX, ADVENTURE_LISTING_CACHE,
    ADVENTURE_LISTING_CACHE_SIZE_MAX, ADVENTURE_QUERY_CACHE
)
from .goal import goal_listing_serialise


EVENT_LOOP = get_event_loop()

if (DB_ENGINE is None):
    COUNTER = iter(count(1))


async def adventure_listing_get_active():
    """
    Gets all the active (non finished) adventures.
    
    This function is a coroutine.
    
    Returns
    -------
    adventures : ``list<Adventure>>``
    """
    results = await query_adventure_listing_get_active()
    
    adventures = []
    
    for result in results:
        entry_id = result['id']
        try:
            adventure = ADVENTURES[entry_id]
        except KeyError:
            adventure = adventure_create_from_entry(result)
            ADVENTURES[entry_id] = adventure
            ADVENTURES_ACTIVE[adventure.user_id] = adventure
        
        try:
            ADVENTURE_CACHE.move_to_end(entry_id)
        except KeyError:
            ADVENTURE_CACHE[entry_id] = adventure
            if len(ADVENTURE_CACHE) > ADVENTURE_CACHE_SIZE_MAX:
                del ADVENTURE_CACHE[next(iter(ADVENTURE_CACHE))]
        
        adventures.append(adventure)
    
    return adventures


async def query_adventure_listing_get_active():
    """
    Queries all the active adventures.
    
    This function is a coroutine.
    
    Returns
    -------
    results : `list<sqlalchemy.engine.result.RowProxy>`
        The entries in the database.
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            ADVENTURE_TABLE.select().where(
                adventure_model.state != ADVENTURE_STATE_FINALISED,
            ),
        )
        
        return await response.fetchall()


if (DB_ENGINE is None):
    @copy_docs(query_adventure_listing_get_active)
    async def query_adventure_listing_get_active():
        return []


async def adventure_save(adventure):
    """
    Updates the adventure's changeable fields in the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to save.
    """
    entry_id = adventure.entry_id
    if entry_id == 0:
        await adventure_save_new(adventure)
        if not adventure.modification_flags:
            return
    
    await query_adventure_save(adventure)
    
    try:
        ADVENTURE_CACHE.move_to_end(entry_id)
    except KeyError:
        ADVENTURE_CACHE[entry_id] = adventure
        if len(ADVENTURE_CACHE) > ADVENTURE_CACHE_SIZE_MAX:
            del ADVENTURE_CACHE[next(iter(ADVENTURE_CACHE))]


async def adventure_save_new(adventure):
    """
    Inserts a new adventure to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to insert.
    """
    user_id = adventure.user_id
    ADVENTURES_ACTIVE[user_id] = adventure
    try:
        entry_id = await query_adventure_save_new(adventure)
        adventure.entry_id = entry_id
    except:
        if ADVENTURES_ACTIVE.get(user_id, None) is adventure:
            del ADVENTURES_ACTIVE[user_id]
        raise
    
    ADVENTURES[entry_id] = adventure
    
    ADVENTURE_CACHE[entry_id] = adventure
    if len(ADVENTURE_CACHE) > ADVENTURE_CACHE_SIZE_MAX:
        del ADVENTURE_CACHE[next(iter(ADVENTURE_CACHE))]
    
    # Remove all the adventure listing page caches of the user.
    keys_to_delete = None
    
    for key in ADVENTURE_LISTING_CACHE.keys():
        if key[0] != user_id:
            continue
        
        if keys_to_delete is None:
            keys_to_delete = []
        
        keys_to_delete.append(key)
        continue
    
    if (keys_to_delete is not None):
        for key in keys_to_delete:
            del ADVENTURE_LISTING_CACHE[key]


async def query_adventure_save_new(adventure):
    """
    Stores the adventure in the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to insert.
    
    Returns
    -------
    entry_id : `int`
        the entry's identifier in the database.
    """
    async with DB_ENGINE.connect() as connector:
        action_listing = adventure.action_listing
        if (action_listing is None):
            action_listing_data = None
        else:
            action_listing_data = adventure_action_listing_serialise(action_listing)
        
        goal_listing = adventure.goal_listing
        if goal_listing is None:
            goal_listing_data = None
        else:
            goal_listing_data = goal_listing_serialise(goal_listing)
        
        adventure.modification_flags = 0
        
        response = await connector.execute(
            ADVENTURE_TABLE.insert().values(
                user_id = adventure.user_id,
                
                location_id = adventure.location_id,
                target_id = adventure.target_id,
                return_id = adventure.return_id,
                auto_cancellation_id = adventure.auto_cancellation_id,
                goal_listing_data = goal_listing_data,
                
                initial_duration_seconds = adventure.initial_duration_seconds,
                created_at = adventure.created_at,
                updated_at = adventure.updated_at,
                action_listing_data = action_listing_data,
                seed = adventure.seed,
                state = adventure.state,
                
                energy_exhausted = adventure.energy_exhausted,
                energy_initial = adventure.energy_initial,
                health_exhausted = adventure.health_exhausted,
                health_initial = adventure.health_initial,
            ).returning(
                adventure_model.id,
            )
        )
        
        result = await response.fetchone()
        return result[0]


if (DB_ENGINE is None):
    @copy_docs(query_adventure_save_new)
    async def query_adventure_save_new(adventure):
        return next(COUNTER)


async def query_adventure_save(adventure):
    """
    Updates the adventure's changeable fields in the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to save.
    """
    modifications = adventure_collect_modifications(adventure)
    if (modifications is None):
        return
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            ADVENTURE_TABLE.update(
                adventure_model.id == adventure.entry_id
            ).values(
                **modifications
            )
        )


if (DB_ENGINE is None):
    @copy_docs(query_adventure_save)
    async def query_adventure_save(adventure):
        adventure.modification_flags = 0
        return


async def adventure_get_active(user_id):
    """
    Gets the user's active adventure.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    adventure : ``None | Adventure``
    """
    return ADVENTURES_ACTIVE.get(user_id, None)


async def adventure_get(adventure_entry_id):
    """
    Gets the adventure for the given entry identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure_entry_id : `int`
        The adventure's entry's identifier in the database.
    
    Returns
    -------
    adventure : ``None | list<Adventure>``
    """
    try:
        adventure = ADVENTURES[adventure_entry_id]
    except KeyError:
        pass
    else:
        try:
            ADVENTURE_CACHE.move_to_end(adventure_entry_id)
        except KeyError:
            ADVENTURE_CACHE[adventure_entry_id] = adventure
            
            if len(ADVENTURE_CACHE) > ADVENTURE_CACHE_SIZE_MAX:
                del ADVENTURE_CACHE[next(iter(ADVENTURE_CACHE))]
        
        return adventure
    
    try:
        task, waiters = ADVENTURE_QUERY_CACHE[adventure_entry_id]
    except KeyError:
        waiters = []
        task = Task(EVENT_LOOP, execute_adventure_get(adventure_entry_id))
        task.add_done_callback(partial_func(_adventure_query_done_callback, adventure_entry_id, waiters))
        ADVENTURE_QUERY_CACHE[adventure_entry_id] = (task, waiters)
    
    waiter = Future(EVENT_LOOP)
    waiters.append(waiter)
    return await waiter


def _adventure_query_done_callback(key, waiters, task):
    """
    Added as a callback of a query to set the result into the waiters and caches the result.
    
    Parameters
    ----------
    key : `int`
        The adventure's entry's identifier in the database used as a key.
    
    waiters : ``list<Future>``
        Result waiters.
    
    task : ``Future``
        The ran task.
    """
    try:
        adventure = task.get_result()
    except BaseException as exception:
        for waiter in waiters:
            waiter.set_exception_if_pending(exception)
    else:
        ADVENTURE_CACHE[key] = adventure
        if len(ADVENTURE_CACHE) > ADVENTURE_CACHE_SIZE_MAX:
            del ADVENTURE_CACHE[next(iter(ADVENTURE_CACHE))]
        
        for waiter in waiters:
            waiter.set_result_if_pending(adventure)
        
    finally:
        del ADVENTURE_QUERY_CACHE[key]


async def execute_adventure_get(adventure_entry_id):
    """
    Queries an adventure's.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure_entry_id : `int`
        The adventure's entry' identifier in the database.
    
    Returns
    -------
    adventure : ``None | Adventure``
    """
    result = await query_adventure_get(adventure_entry_id)
    if result is None:
        adventure = None
    else:
        adventure = adventure_create_from_entry(result)
        ADVENTURES[adventure.entry_id] = adventure
    
    return adventure


async def query_adventure_get(adventure_entry_id):
    """
    Queries an adventure's.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure_entry_id : `int`
        The adventure's entry' identifier in the database.
    
    Returns
    -------
    result : `None | sqlalchemy.engine.result.RowProxy`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            ADVENTURE_TABLE.select().where(
                adventure_model.id == adventure_entry_id,
            ),
        )
        
        return await response.fetchone()


if DB_ENGINE is None:
    @copy_docs(query_adventure_get)
    async def query_adventure(query_adventure_get):
        return None


async def adventure_listing_get_page(user_id, page_index, page_size):
    """
    Get the given adventure listing page from the database.
    
    Parameters
    ----------
    user_id : `int`
        The owner user's identifier.
    
    page_index : `int`
        The page's index.
        If passed as negative, returns the last page.
    
    page_size : `int`
        The size of the page to get.
    
    Returns
    -------
    page_count_and_adventure_listing : ``(int, None | list<Adventure>)``
    """
    key = (user_id, page_index, page_size)
    
    try:
        page_count_and_adventure_listing = ADVENTURE_LISTING_CACHE[key]
    except KeyError:
        pass
    else:
        ADVENTURE_LISTING_CACHE.move_to_end(key)
        return page_count_and_adventure_listing
    
    page_count, results = await query_adventure_listing_get_page(user_id, page_index, page_size)
    if not results:
        adventure_listing = None
    
    else:
        adventure_listing = []
        
        for result in results:
            adventure_entry_id = result['id']
            
            try:
                adventure = ADVENTURES[adventure_entry_id]
            except KeyError:
                adventure = adventure_create_from_entry(result)
                ADVENTURES[adventure_entry_id] = adventure
            
            adventure_listing.append(adventure)
    
    page_count_and_adventure_listing = (page_count, adventure_listing)
    ADVENTURE_LISTING_CACHE[key] = page_count_and_adventure_listing
    
    if len(ADVENTURE_LISTING_CACHE) > ADVENTURE_LISTING_CACHE_SIZE_MAX:
        del ADVENTURE_LISTING_CACHE[next(iter(ADVENTURE_LISTING_CACHE))]
    
    if page_index < 0:
        alternative_key = (user_id, page_count - 1, page_size)
        ADVENTURE_LISTING_CACHE[alternative_key] = page_count_and_adventure_listing
        
        if len(ADVENTURE_LISTING_CACHE) > ADVENTURE_LISTING_CACHE_SIZE_MAX:
            del ADVENTURE_LISTING_CACHE[next(iter(ADVENTURE_LISTING_CACHE))]
        
    
    return page_count_and_adventure_listing


async def query_adventure_listing_get_page(user_id, page_index, page_size):
    """
    Queries the given adventure listing page from the database.
    
    Parameters
    ----------
    user_id : `int`
        The owner user's identifier.
    
    page_index : `int`
        The page's index.
        If passed as negative, returns the last page.
    
    page_size : `int`
        The size of the page to get.
    
    Returns
    -------
    page_count_and_results : `(int, list<sqlalchemy.engine.result.RowProxy>)`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                     alchemy_function.count().label('entry_count'),
                ],
            ).where(
                adventure_model.user_id == user_id,
            )
        )
        
        result = await response.fetchone()
        entry_count = result[0]
        
        if entry_count == 0:
            return 1, []
        
        page_count = (entry_count + page_size - 1) // page_size
        
        if page_index >= page_count:
            return page_count, []
        
        if page_index < 0:
            page_index = page_count - 1
        
        response = await connector.execute(
            ADVENTURE_TABLE.select().where(
                adventure_model.user_id == user_id,
            ).order_by(
                asc(adventure_model.created_at),
            ).limit(
                page_size,
            ).offset(
                page_size * page_index,
            )
        )
        
        results = await response.fetchall()
        return page_count, results


if DB_ENGINE is None:
    @copy_docs(query_adventure_listing_get_page)
    async def query_adventure_listing_get_page(user_id, page_index, page_size):
        return 1, []
