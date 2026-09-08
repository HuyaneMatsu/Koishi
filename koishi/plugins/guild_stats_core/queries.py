__all__ = ('guild_stats_get', 'guild_stats_save')

from functools import partial as partial_func
from itertools import count

from scarletio import Future, Task, copy_docs, get_event_loop, shield

from ...bot_utils.models import DB_ENGINE, GUILD_STATS_TABLE, guild_stats_model

from .constants import (
    GUILD_STATS, GUILD_STATS_CACHE, GUILD_STATS_CACHE_SIZE, GUILD_STATS_QUERY_TASKS, GUILD_STATS_SAVE_TASKS
)
from .guild_stats import (
    GuildStats, guild_stats_collect_modifications, guild_stats_create, guild_stats_create_from_entry
)


if (DB_ENGINE is None):
    COUNTER = iter(count(1))

EVENT_LOOP = get_event_loop()


async def guild_stats_get(guild_id):
    """
    Gets the stats for the given guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild_id : `int`
        Guild's identifier.
    
    Returns
    -------
    guild_stat : ``GuildStats``
    """
    try:
        guild_stats = GUILD_STATS[guild_id]
    except KeyError:
        pass
    else:
        try:
            GUILD_STATS_CACHE.move_to_end(guild_id)
        except KeyError:
            GUILD_STATS_CACHE[guild_id] = guild_stats
            if len(GUILD_STATS_CACHE) > GUILD_STATS_CACHE_SIZE:
                del GUILD_STATS_CACHE[next(iter(GUILD_STATS_CACHE))]
        
        return guild_stats
    
    try:
        task, waiters = GUILD_STATS_QUERY_TASKS[guild_id]
    except KeyError:
        waiters = []
        task = Task(EVENT_LOOP, execute_guild_stats_get(guild_id))
        task.add_done_callback(partial_func(_guild_stats_query_done_callback, guild_id, waiters))
        GUILD_STATS_QUERY_TASKS[guild_id] = (task, waiters)
    
    waiter = Future(EVENT_LOOP)
    waiters.append(waiter)
    return await waiter
    
    return await shield(task, KOKORO)


def _guild_stats_query_done_callback(key, waiters, task):
    """
    Added as a callback of a query to set the result into the waiters and caches the result.
    
    Parameters
    ----------
    key : `int`
        The guild_stats's entry's identifier in the database used as a key.
    
    waiters : ``list<Future>``
        Result waiters.
    
    task : ``Future``
        The ran task.
    """
    try:
        guild_stats = task.get_result()
    except BaseException as exception:
        for waiter in waiters:
            waiter.set_exception_if_pending(exception)
    else:
        GUILD_STATS[key] = guild_stats
        GUILD_STATS_CACHE[key] = guild_stats
        if len(GUILD_STATS_CACHE) > GUILD_STATS_CACHE_SIZE:
            del GUILD_STATS_CACHE[next(iter(GUILD_STATS_CACHE))]
        
        for waiter in waiters:
            waiter.set_result_if_pending(guild_stats)
        
    finally:
        del GUILD_STATS_QUERY_TASKS[key]


async def execute_guild_stats_get(guild_id):
    """
    Queries a guild stats.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild_id : `int`
        Guild's identifier.
    
    Returns
    -------
    guild_stats : ``GuildStats``
    """
    result = await query_guild_stats_get(guild_id)
    if result is None:
        guild_stats = guild_stats_create(guild_id)
    else:
        guild_stats = guild_stats_create_from_entry(result)
    
    return guild_stats


async def query_guild_stats_get(guild_id):
    """
    Queries the stats for the given guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild_id : `int`
        Guild's identifier.
    
    Returns
    -------
    result : `None | sqlalchemy.engine.result.RowProxy`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            GUILD_STATS_TABLE.select().where(
                guild_stats_model.guild_id == guild_id,
            ),
        )
        
        return await response.fetchone()


if DB_ENGINE is None:
    @copy_docs(query_guild_stats_get)
    async def query_guild_stats_get(guild_id):
        return None


async def guild_stats_save(guild_stats):
    """
    Saves the guild stats.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild_stats : ``GuildStats``
        Guild stats to save.
    """
    try:
        task = GUILD_STATS_SAVE_TASKS[guild_stats.guild_id]
    except KeyError:
        GUILD_STATS_SAVE_TASKS[guild_stats.guild_id] = task = Task(EVENT_LOOP, query_guild_stats_save_loop(guild_stats))
    
    await shield(task, EVENT_LOOP)


async def query_guild_stats_save_loop(guild_stats):
    """
    Runs the entry proxy saver.
    
    This method is a coroutine.
    
    Parameters
    ----------
    guild_stats : ``GuildStats``
        Guild stats to save.
    """
    try:
        async with DB_ENGINE.connect() as connector:
            entry_id = guild_stats.entry_id
            # If the entry is new, insert it.
            if (entry_id == 0):
                guild_stats.modification_flags = 0
                response = await connector.execute(
                    GUILD_STATS_TABLE.insert().values(
                        guild_id = guild_stats.guild_id,
                        
                        credibility = guild_stats.credibility,
                    ).returning(
                        guild_stats_model.id,
                    )
                )
                
                result = await response.fetchone()
                guild_stats.entry_id = result[0]
            
            while True:
                modifications = guild_stats_collect_modifications(guild_stats)
                if (modifications is None):
                    break
                
                await connector.execute(
                    GUILD_STATS_TABLE.update(
                        guild_stats_model.id == entry_id,
                    ).values(
                        **modifications
                    )
                )
                continue
        
    finally:
        try:
            del GUILD_STATS_SAVE_TASKS[guild_stats.guild_id]
        except KeyError:
            pass


if (DB_ENGINE is None):
    @copy_docs(query_guild_stats_save_loop)
    async def query_guild_stats_save_loop(guild_stats):
        guild_stats.modification_flags = 0
        if not guild_stats.entry_id:
            guild_stats.entry_id = next(COUNTER)
