__all__ = ('user_stats_get', 'user_stats_save')

from functools import partial as partial_func
from itertools import count

from scarletio import Future, Task, copy_docs, get_event_loop, shield

from ...bot_utils.models import DB_ENGINE, USER_STATS_TABLE, user_stats_model

from .constants import (
    USER_STATS, USER_STATS_CACHE, USER_STATS_CACHE_SIZE, USER_STATS_QUERY_TASKS, USER_STATS_SAVE_TASKS
)
from .user_stats import UserStats, user_stats_collect_modifications, user_stats_create, user_stats_create_from_entry


if (DB_ENGINE is None):
    COUNTER = iter(count(1))

EVENT_LOOP = get_event_loop()


async def user_stats_get(user_id):
    """
    Gets the stats for the given user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    user_stat : ``UserStats``
    """
    try:
        user_stats = USER_STATS[user_id]
    except KeyError:
        pass
    else:
        try:
            USER_STATS_CACHE.move_to_end(user_id)
        except KeyError:
            USER_STATS_CACHE[user_id] = user_stats
            if len(USER_STATS_CACHE) > USER_STATS_CACHE_SIZE:
                del USER_STATS_CACHE[next(iter(USER_STATS_CACHE))]
        
        return user_stats
    
    try:
        task, waiters = USER_STATS_QUERY_TASKS[user_id]
    except KeyError:
        waiters = []
        task = Task(EVENT_LOOP, execute_user_stats_get(user_id))
        task.add_done_callback(partial_func(_user_stats_query_done_callback, user_id, waiters))
        USER_STATS_QUERY_TASKS[user_id] = (task, waiters)
    
    waiter = Future(EVENT_LOOP)
    waiters.append(waiter)
    return await waiter
    
    return await shield(task, KOKORO)


def _user_stats_query_done_callback(key, waiters, task):
    """
    Added as a callback of a query to set the result into the waiters and caches the result.
    
    Parameters
    ----------
    key : `int`
        The user_stats's entry's identifier in the database used as a key.
    
    waiters : ``list<Future>``
        Result waiters.
    
    task : ``Future``
        The ran task.
    """
    try:
        user_stats = task.get_result()
    except BaseException as exception:
        for waiter in waiters:
            waiter.set_exception_if_pending(exception)
    else:
        USER_STATS[key] = user_stats
        USER_STATS_CACHE[key] = user_stats
        if len(USER_STATS_CACHE) > USER_STATS_CACHE_SIZE:
            del USER_STATS_CACHE[next(iter(USER_STATS_CACHE))]
        
        for waiter in waiters:
            waiter.set_result_if_pending(user_stats)
        
    finally:
        del USER_STATS_QUERY_TASKS[key]


async def execute_user_stats_get(user_id):
    """
    Queries a user stats.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    user_stats : ``UserStats``
    """
    result = await query_user_stats_get(user_id)
    if result is None:
        user_stats = user_stats_create(user_id)
    else:
        user_stats = user_stats_create_from_entry(result)
    
    return user_stats


async def query_user_stats_get(user_id):
    """
    Queries the stats for the given user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    result : `None | sqlalchemy.engine.result.RowProxy`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            USER_STATS_TABLE.select().where(
                user_stats_model.user_id == user_id,
            ),
        )
        
        return await response.fetchone()


if DB_ENGINE is None:
    @copy_docs(query_user_stats_get)
    async def query_user_stats_get(user_id):
        return None


async def user_stats_save(user_stats):
    """
    Saves the user stats.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to save.
    """
    try:
        task = USER_STATS_SAVE_TASKS[user_stats.user_id]
    except KeyError:
        USER_STATS_SAVE_TASKS[user_stats.user_id] = task = Task(EVENT_LOOP, query_user_stats_save_loop(user_stats))
    
    await shield(task, EVENT_LOOP)


async def query_user_stats_save_loop(user_stats):
    """
    Runs the entry proxy saver.
    
    This method is a coroutine.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to save.
    """
    try:
        async with DB_ENGINE.connect() as connector:
            entry_id = user_stats.entry_id
            # If the entry is new, insert it.
            if (entry_id == 0):
                user_stats.modification_flags = 0
                response = await connector.execute(
                    USER_STATS_TABLE.insert().values(
                        user_id = user_stats.user_id,
                        
                        stat_housewife = user_stats.stat_housewife,
                        stat_cuteness = user_stats.stat_cuteness,
                        stat_bedroom = user_stats.stat_bedroom,
                        stat_charm = user_stats.stat_charm,
                        stat_loyalty = user_stats.stat_loyalty,
                        
                        credibility = user_stats.credibility,
                        recovering_until = user_stats.recovering_until,
                        recovering_until_notification_at = user_stats.recovering_until_notification_at,
                        
                        item_id_costume = user_stats.item_id_costume,
                        item_id_head = user_stats.item_id_head,
                        item_id_species = user_stats.item_id_species,
                        item_id_weapon = user_stats.item_id_weapon,
                    ).returning(
                        user_stats_model.id,
                    )
                )
                
                result = await response.fetchone()
                user_stats.entry_id = result[0]
            
            while True:
                modifications = user_stats_collect_modifications(user_stats)
                if (modifications is None):
                    break
                
                await connector.execute(
                    USER_STATS_TABLE.update(
                        user_stats_model.id == entry_id,
                    ).values(
                        **modifications
                    )
                )
                continue
        
    finally:
        try:
            del USER_STATS_SAVE_TASKS[user_stats.user_id]
        except KeyError:
            pass


if (DB_ENGINE is None):
    @copy_docs(query_user_stats_save_loop)
    async def query_user_stats_save_loop(user_stats):
        user_stats.modification_flags = 0
        if not user_stats.entry_id:
            user_stats.entry_id = next(COUNTER)
