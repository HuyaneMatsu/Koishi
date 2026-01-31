__all__ = (
    'delete_relationship_request', 'get_relationship_request', 'get_relationship_request_listing',
    'save_relationship_request'
)

from functools import partial as partial_func
from itertools import count

from hata import KOKORO
from scarletio import Future, Task, copy_docs, get_event_loop, shield

from ...bot_utils.models import DB_ENGINE, RELATIONSHIP_REQUEST_TABLE, relationship_request_model

from .constants import (
    RELATIONSHIP_REQUEST_LISTING_CACHE, RELATIONSHIP_REQUEST_LISTING_CACHE_SIZE_MAX, RELATIONSHIP_REQUEST_LISTING_GET_QUERY_TASKS,
    RELATIONSHIP_REQUEST_SAVE_TASKS, RELATIONSHIP_REQUEST_CACHE, RELATIONSHIP_REQUEST_QUERY_TASKS
)
from .relationship_request import RelationshipRequest

EVENT_LOOP = get_event_loop()


if (DB_ENGINE is None):
    COUNTER = iter(count(1))


def _relationship_request_listing_query_done_callback(key, waiters, task):
    """
    Added as a callback of a query to set the result into the waiters and caches the result.
    
    Parameters
    ----------
    key : `int`
        The user's identifier used as a key.
    
    waiters : ``list<Future>``
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
        RELATIONSHIP_REQUEST_LISTING_CACHE[key] = listing
        if len(RELATIONSHIP_REQUEST_LISTING_CACHE) > RELATIONSHIP_REQUEST_LISTING_CACHE_SIZE_MAX:
            del RELATIONSHIP_REQUEST_LISTING_CACHE[next(iter(RELATIONSHIP_REQUEST_LISTING_CACHE))]
        
        for waiter in waiters:
            waiter.set_result_if_pending(listing)
        
    finally:
        del RELATIONSHIP_REQUEST_LISTING_GET_QUERY_TASKS[key]


async def get_relationship_request_listing(user_id, outgoing):
    """
    Gets the user's relationship requests.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    outgoing : `bool`
        Whether to query for the outgoing requests.
    
    Returns
    -------
    relationship_request_listing : ``None | list<RelationshipRequest>``
    """
    listing_key = user_id, outgoing
    
    try:
        listing = RELATIONSHIP_REQUEST_LISTING_CACHE[listing_key]
    except KeyError:
        pass
    else:
        RELATIONSHIP_REQUEST_LISTING_CACHE.move_to_end(listing_key)
        return listing
    
    try:
        task, waiters = RELATIONSHIP_REQUEST_LISTING_GET_QUERY_TASKS[listing_key]
    except KeyError:
        waiters = []
        task = Task(EVENT_LOOP, query_relationship_request_listing(user_id, outgoing))
        task.add_done_callback(partial_func(_relationship_request_listing_query_done_callback, listing_key, waiters))
        RELATIONSHIP_REQUEST_LISTING_GET_QUERY_TASKS[listing_key] = (task, waiters)
    
    waiter = Future(EVENT_LOOP)
    waiters.append(waiter)
    return await waiter


async def query_relationship_request_listing(user_id, outgoing):
    """
    queries the user's relationship_requests.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    relationship_request_listing : ``None | list<RelationshipRequest>``
    """
    if outgoing:
        user_id_member = relationship_request_model.source_user_id
    else:
        user_id_member = relationship_request_model.target_user_id
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            RELATIONSHIP_REQUEST_TABLE.select().where(
                user_id_member == user_id,
            ),
        )
        
        results = await response.fetchall()
        if not results:
            relationship_request_listing = None
        
        else:
            relationship_request_listing = []
            
            for result in results:
                entry_id = result['id']
                try:
                    relationship_request = RELATIONSHIP_REQUEST_CACHE[entry_id]
                except KeyError:
                    relationship_request = RelationshipRequest.from_entry(result)
                    RELATIONSHIP_REQUEST_CACHE[entry_id] = relationship_request
                
                relationship_request_listing.append(relationship_request)
    
    return relationship_request_listing


if DB_ENGINE is None:
    @copy_docs(query_relationship_request_listing)
    async def query_relationship_request_listing(user_id, outgoing):
        return None


async def save_relationship_request(relationship_request):
    """
    Saves the user stats.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship_request : ``RelationshipRequest``
        Relationship request to save.
    """
    key = (relationship_request.source_user_id, relationship_request.target_user_id)
    
    try:
        task = RELATIONSHIP_REQUEST_SAVE_TASKS[key]
    except KeyError:
        RELATIONSHIP_REQUEST_SAVE_TASKS[key] = task = Task(
            EVENT_LOOP, query_save_relationship_request_loop(relationship_request)
        )
    
    await shield(task, EVENT_LOOP)


async def query_save_relationship_request_loop(relationship_request):
    """
    Runs the entry proxy saver.
    
    This method is a coroutine.
    
    Parameters
    ----------
    relationship_request : ``RelationshipRequest``
        Relationship request to save.
    """
    try:
        async with DB_ENGINE.connect() as connector:
            entry_id = relationship_request.entry_id
            # If the entry is new, insert it.
            if (entry_id == 0):
                relationship_request.modified_fields = None
                response = await connector.execute(
                    RELATIONSHIP_REQUEST_TABLE.insert().values(
                        investment = relationship_request.investment,
                        relationship_type = relationship_request.relationship_type,
                        source_user_id = relationship_request.source_user_id,
                        target_user_id = relationship_request.target_user_id,
                    ).returning(
                        relationship_request_model.id,
                    )
                )
                
                result = await response.fetchone()
                relationship_request.entry_id = result[0]
                _insert_relationship_request_to_cache(relationship_request)
            
            modified_fields = relationship_request.modified_fields
            while (modified_fields is not None):
                relationship_request.modified_fields = None
                
                await connector.execute(
                    RELATIONSHIP_REQUEST_TABLE.update(
                        relationship_request_model.id == entry_id,
                    ).values(
                        **modified_fields
                    )
                )
                modified_fields = relationship_request.modified_fields
                continue
        
    finally:
        try:
            del RELATIONSHIP_REQUEST_SAVE_TASKS[
                relationship_request.source_user_id, relationship_request.target_user_id
            ]
        except KeyError:
            pass


if (DB_ENGINE is None):
    @copy_docs(query_save_relationship_request_loop)
    async def query_save_relationship_request_loop(relationship_request):
        try:
            relationship_request.modified_fields = None
            if not relationship_request.entry_id:
                relationship_request.entry_id = next(COUNTER)
                _insert_relationship_request_to_cache(relationship_request)
        
        finally:
            try:
                del RELATIONSHIP_REQUEST_SAVE_TASKS[
                    relationship_request.source_user_id, relationship_request.target_user_id
                ]
            except KeyError:
                pass


def _insert_relationship_request_to_cache(relationship_request):
    """
    Inserts the relationship request to the cache.
    
    Parameters
    ----------
    relationship_request : ``RelationshipRequest``
        The relationship request to insert.
    """
    RELATIONSHIP_REQUEST_CACHE[relationship_request.entry_id] = relationship_request
    
    for listing_key in ((relationship_request.source_user_id, True), (relationship_request.target_user_id, False)):
        try:
            listing = RELATIONSHIP_REQUEST_LISTING_CACHE[listing_key]
        except KeyError:
            if (DB_ENGINE is not None):
                continue
            
            listing = None
        
        if (listing is None):
            RELATIONSHIP_REQUEST_LISTING_CACHE[listing_key] = [relationship_request]
            continue
        
        if (relationship_request not in listing):
            listing.append(relationship_request)
        
        continue


async def delete_relationship_request(relationship_request):
    """
    Deletes the relationship request from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship_request : ``RelationshipRequest``
        The relationship request to delete.
    """
    if not relationship_request.entry_id:
        return
    
    await query_delete_relationship_request(relationship_request)

    try:
        del RELATIONSHIP_REQUEST_CACHE[relationship_request.entry_id]
    except KeyError:
        pass
    
    for listing_key in ((relationship_request.source_user_id, True), (relationship_request.target_user_id, False)):
        try:
            listing = RELATIONSHIP_REQUEST_LISTING_CACHE[listing_key]
        except KeyError:
            continue
        
        if (listing is None):
            continue
        
        try:
            listing.remove(relationship_request)
        except ValueError:
            continue
        
        if listing:
            continue
        
        RELATIONSHIP_REQUEST_LISTING_CACHE[listing_key] = None
        continue


async def query_delete_relationship_request(relationship_request):
    """
    Executes a query to delete the relationship request from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship_request : ``RelationshipRequest``
        The relationship request to delete.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            RELATIONSHIP_REQUEST_TABLE.delete().where(
                relationship_request_model.id == relationship_request.entry_id
            ),
        )


if (DB_ENGINE is None):
    @copy_docs(query_delete_relationship_request)
    async def query_delete_relationship_request(relationship_request):
        pass


async def get_relationship_request(entry_id):
    """
    Gets a single relationship request for the given entry identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry_id : `int`
        Entry identifier.
    
    Returns
    -------
    relationship_request : ``None | RelationshipRequest``
    """
    try:
        relationship_request = RELATIONSHIP_REQUEST_CACHE[entry_id]
    except KeyError:
        pass
    else:
        return relationship_request
    
    try:
        task, waiters = RELATIONSHIP_REQUEST_QUERY_TASKS[entry_id]
    except KeyError:
        waiters = []
        task = Task(KOKORO, query_relationship_request(entry_id, waiters))
        RELATIONSHIP_REQUEST_QUERY_TASKS[entry_id] = (task, waiters)
    
    waiter = Future(KOKORO)
    waiters.append(waiter)
    
    return (await waiter)


async def query_relationship_request(entry_id, waiters):
    """
    Gets a single relationship request for the given entry identifier from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry_id : `int`
        Entry identifier.
    
    waiters : ``list<Future>``
        Result waiters.
    """
    try:
        async with DB_ENGINE.connect() as connector:
            response = await connector.execute(
                RELATIONSHIP_REQUEST_TABLE.select().where(
                    relationship_request_model.id == entry_id,
                ),
            )
            
            result = await response.fetchone()
            if result is None:
                relationship_request = None
            else:
                relationship_request = RelationshipRequest.from_entry(result)
                RELATIONSHIP_REQUEST_CACHE[entry_id] = relationship_request
            
    except BaseException as exception:
        for waiter in waiters:
            waiter.set_exception_if_pending(exception)
        raise
    
    else:
        for waiter in waiters:
            waiter.set_result_if_pending(relationship_request)
    
    finally:
        try:
            del RELATIONSHIP_REQUEST_QUERY_TASKS[entry_id]
        except KeyError:
            pass


if (DB_ENGINE is None):
    @copy_docs(query_relationship_request)
    async def query_relationship_request(entry_id, waiters):
        try:
            for waiter in waiters:
                waiter.set_result_if_pending(None)
            
        finally:
            try:
                del RELATIONSHIP_REQUEST_QUERY_TASKS[entry_id]
            except KeyError:
                pass
