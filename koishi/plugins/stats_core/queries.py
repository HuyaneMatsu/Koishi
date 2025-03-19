__all__ = ('get_stats',)

from scarletio import copy_docs

from ...bot_utils.models import DB_ENGINE, STATS_TABLE, stats_model

from .constants import STATS_CACHE, STATS_CACHE_SIZE_MAX
from .stats import Stats


async def get_stats(user_id):
    """
    Gets the stats for the given user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    entries : ``Stats``
    """
    try:
        listing = STATS_CACHE[user_id]
    except KeyError:
        pass
    else:
        STATS_CACHE.move_to_end(user_id)
        return listing
    
    listing = await query_stats(user_id)
    STATS_CACHE[user_id] = listing
    if len(STATS_CACHE) > STATS_CACHE_SIZE_MAX:
        del STATS_CACHE[next(iter(STATS_CACHE))]
    
    return listing


async def query_stats(user_id):
    """
    Queries the stats for the given user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    stat : ``Stats``
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            STATS_TABLE.select().where(
                stats_model.user_id == user_id,
            ),
        )
        
        result = await response.fetchone()
        if result is None:
            stats = Stats(user_id)
        else:
            stats = Stats.from_entry(result)
    
    return stats


if DB_ENGINE is None:
    @copy_docs(query_stats)
    async def query_stats(user_id):
        return Stats(user_id)
