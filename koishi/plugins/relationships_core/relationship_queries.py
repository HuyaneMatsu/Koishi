__all__ = ('get_relationship_listing', 'get_relationship_listing_with_extend')

from functools import partial as partial_func

from scarletio import Future, Task, copy_docs, get_event_loop
from sqlalchemy import or_

from ...bot_utils.models import DB_ENGINE, RELATIONSHIP_TABLE, relationship_model

from .constants import (
    RELATIONSHIP_LISTING_CACHE, RELATIONSHIP_LISTING_CACHE_SIZE_MAX, RELATIONSHIP_LISTING_GET_QUERY_TASKS
)
from .relationship import Relationship
from .relationship_types import RELATIONSHIP_TYPE_NONE, RELATIONSHIP_TYPE_RELATIONSHIPS, RELATION_TYPE_ALLOWED_EXTENDS


EVENT_LOOP = get_event_loop()


def _relationship_listing_query_done_callback(key, waiters, task):
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
        listing = task.get_result()
    except BaseException as exception:
        for waiter in waiters:
            waiter.set_exception_if_pending(exception)
    else:
        RELATIONSHIP_LISTING_CACHE[key] = listing
        if len(RELATIONSHIP_LISTING_CACHE) > RELATIONSHIP_LISTING_CACHE_SIZE_MAX:
            del RELATIONSHIP_LISTING_CACHE[next(iter(RELATIONSHIP_LISTING_CACHE))]
        
        for waiter in waiters:
            waiter.set_result_if_pending(listing)
        
    finally:
        del RELATIONSHIP_LISTING_GET_QUERY_TASKS[key]


async def get_relationship_listing(user_id):
    """
    Gets the user's relationships.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    relationship_listing : `None | list<Relationship>`
    """
    try:
        listing = RELATIONSHIP_LISTING_CACHE[user_id]
    except KeyError:
        pass
    else:
        RELATIONSHIP_LISTING_CACHE.move_to_end(user_id)
        return listing
    
    try:
        task, waiters = RELATIONSHIP_LISTING_GET_QUERY_TASKS[user_id]
    except KeyError:
        waiters = []
        task = Task(EVENT_LOOP, query_relationship_listing(user_id))
        task.add_done_callback(partial_func(_relationship_listing_query_done_callback, user_id, waiters))
        RELATIONSHIP_LISTING_GET_QUERY_TASKS[user_id] = (task, waiters)
    
    waiter = Future(EVENT_LOOP)
    waiters.append(waiter)
    return await waiter


def _select_extended_relationships(
    connector_user_id,
    allowed_relationship_types,
    relationship_listing,
    mentioned_user_ids,
):
    """
    Selects the extended relationships.
    
    Parameters
    ----------
    connector_user_id : `int`
        The connector user's identifier.
    
    allowed_relationship_types : `tuple<int>`
        The allowed relationship types to be connected.
    
    relationship_listing : `list<Relationship>`
        The waifu user's relationships.
    
    mentioned_user_ids : `set<int>`
        A set of user identifiers to avoid repeats.
    
    Returns
    -------
    extra : `None | list<Relationship>`
    """
    extra = None
    
    for relationship in relationship_listing:
        # Exclude duplicate users.
        related_id = relationship.source_user_id
        relationship_type = relationship.relationship_type
        if related_id == connector_user_id:
            related_id = relationship.target_user_id
            relationship_type = RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
        
        if relationship_type not in allowed_relationship_types:
            continue
        
        # Exclude if the user is already related.
        if related_id in mentioned_user_ids:
            continue
        
        mentioned_user_ids.add(related_id)
        if extra is None:
            extra = []
            
        extra.append(relationship)
    
    return extra


async def get_relationship_listing_with_extend(user_id):
    """
    Gets the user's extended relationship listing.
    The extend is separated by the relationships they are branching out form.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    relationship_listing_with_extend : `None | list<(Relationship, None | list<Relationship>)>`
    """
    user_relationship_listing = await get_relationship_listing(user_id)
    if (user_relationship_listing is None):
        return None
    
    mentioned_user_ids = set()
    for relationship in user_relationship_listing:
        mentioned_user_ids.add(relationship.source_user_id)
        mentioned_user_ids.add(relationship.target_user_id)
    
    relationship_listing_with_extend = []
    
    for relationship in user_relationship_listing:
        connector_user_id = relationship.source_user_id
        relationship_type = relationship.relationship_type
        if connector_user_id == user_id:
            connector_user_id = relationship.target_user_id
            relationship_type = RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
        
        allowed_relationship_types = RELATION_TYPE_ALLOWED_EXTENDS.get(relationship_type, None)
        if allowed_relationship_types is None:
            extend = None
        else:
            relationship_listing = await get_relationship_listing(connector_user_id)
            if (relationship_listing is None) or (len(relationship_listing) == 1):
                extend = None
            else:
                extend = _select_extended_relationships(
                    connector_user_id,
                    allowed_relationship_types,
                    relationship_listing,
                    mentioned_user_ids,
                )
        
        relationship_listing_with_extend.append((relationship, extend))
    
    return relationship_listing_with_extend


async def query_relationship_listing(user_id):
    """
    queries the user's relationships.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    relationship_listing : `None | list<Relationship>`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            RELATIONSHIP_TABLE.select().where(
                or_(
                    relationship_model.source_user_id == user_id,
                    relationship_model.target_user_id == user_id,
                ),  
            ),
        )
        
        results = await response.fetchall()
        if results:
            relationships = [Relationship.from_entry(result) for result in results]
        else:
            relationships = None
    
    return relationships


if DB_ENGINE is None:
    @copy_docs(query_relationship_listing)
    async def query_relationship_listing(user_id):
        return None
