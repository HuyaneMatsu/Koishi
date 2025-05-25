__all__ = ('get_guild_stats',)

from hata import KOKORO
from scarletio import Future, Task, copy_docs

from ...bot_utils.models import DB_ENGINE, GUILD_STATS_TABLE, guild_stats_model

from .constants import GUILD_STATS_CACHE, GUILD_STATS_QUERY_TASKS
from .guild_stats import GuildStats


async def get_guild_stats(guild_id):
    """
    Gets the stats of the given guild for their identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier.
    
    Returns
    -------
    guild_stats : ``GuildStats``
    """
    guild_stats = _get_guild_stats_from_cache(guild_id)
    if (guild_stats is not None):
        return guild_stats
    
    waiter = _get_guild_stats_query_waiter(guild_id)
    if waiter is None:
        waiter = _create_guild_stats_query_waiter(guild_id)
    
    return (await waiter)


def _get_guild_stats_from_cache(guild_id):
    """
    Gets the guild stats from cache.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to get the stats for.
    
    Returns
    -------
    guild_stats : `None | GuildStats`
    """
    try:
        guild_stats = GUILD_STATS_CACHE[guild_id]
    except KeyError:
        return None
    
    GUILD_STATS_CACHE.move_to_end(guild_id)
    return guild_stats


def _get_guild_stats_query_waiter(guild_id):
    """
    Returns a guild stats waiter. If there is no waiter yet, returns `None`.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to get the stats for.
    
    Returns
    -------
    waiter : `None | Future`
    """
    try:
        task, waiters = GUILD_STATS_QUERY_TASKS[guild_id]
    except KeyError:
        return None
    
    waiter = Future(KOKORO)
    waiters.append(waiter)
    return waiter


def _create_guild_stats_query_waiter(guild_id):
    """
    Creates a guild stats query waiter. Use it after `_get_guild_stats_query_waiter`.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to get the stats for.
    
    Returns
    -------
    waiter : `Future`
    """
    waiters = []
    task = Task(KOKORO, query_guild_stats(guild_id, waiters))
    GUILD_STATS_QUERY_TASKS[guild_id] = (task, waiters)
    waiter = Future(KOKORO)
    waiters.append(waiter)
    return waiter


async def query_guild_stats(guild_id, waiters):
    """
    Requests a guild stats entry from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier to query for.
    
    waiters : `list<Future>`
        Result waiters.
    """
    try:
        async with DB_ENGINE.connect() as connector:
            response = await connector.execute(
                GUILD_STATS_TABLE.select().where(
                    guild_stats_model.guild_id == guild_id,
                ),
            )
            
            result = await response.fetchone()
            if result is None:
                guild_stats = GuildStats(guild_id)
            else:
                guild_stats = GuildStats.from_entry(result)
        
    except BaseException as exception:
        for waiter in waiters:
            waiter.set_exception_if_pending(exception)
        raise
    
    else:
        for waiter in waiters:
            waiter.set_result_if_pending(guild_stats)
    
    finally:
        try:
            del GUILD_STATS_QUERY_TASKS[guild_id]
        except KeyError:
            pass


if (DB_ENGINE is None):
    @copy_docs(query_guild_stats)
    async def query_guild_stats(guild_id, waiters):
        try:
            guild_stats = GuildStats(guild_id)
            
            for waiter in waiters:
                waiter.set_result_if_pending(guild_stats)
        
        finally:
            try:
                del GUILD_STATS_QUERY_TASKS[guild_id]
            except KeyError:
                pass
