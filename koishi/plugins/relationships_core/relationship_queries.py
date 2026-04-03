__all__ = (
    'delete_relationship', 'get_relationship_extension_traces', 'get_relationship_listing',
    'get_relationship_listings', 'save_relationship'
)

from functools import partial as partial_func
from itertools import count

from scarletio import Future, Task, TaskGroup, copy_docs, get_event_loop, shield
from sqlalchemy import or_

from ...bot_utils.models import DB_ENGINE, RELATIONSHIP_TABLE, relationship_model

from .constants import (
    RELATIONSHIP_CACHE, RELATIONSHIP_LISTING_CACHE, RELATIONSHIP_LISTING_CACHE_SIZE_MAX,
    RELATIONSHIP_LISTING_GET_QUERY_TASKS, RELATIONSHIP_SAVE_TASKS
)
from .relationship import Relationship
from .relationship_extension_trace import RelationshipExtensionTrace
from .relationship_types import (
    RELATIONSHIP_TYPES_EXTENDABLE, RELATIONSHIP_TYPE_NONE, RELATIONSHIP_TYPE_RELATIONSHIPS,
    RELATIONSHIP_TYPE_SISTER_RELATIVE, RELATION_TYPE_ALLOWED_EXTENDS, RELATION_TYPE_EXTENSIONS,
    determine_relative_sister, do_relationship_type_flip_basic
)


EVENT_LOOP = get_event_loop()


if (DB_ENGINE is None):
    COUNTER = iter(count(1))


def _relationship_listing_query_done_callback(key, waiters, task):
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
        relationship_listing = task.get_result()
    except BaseException as exception:
        for waiter in waiters:
            waiter.set_exception_if_pending(exception)
    else:
        RELATIONSHIP_LISTING_CACHE[key] = relationship_listing
        if len(RELATIONSHIP_LISTING_CACHE) > RELATIONSHIP_LISTING_CACHE_SIZE_MAX:
            del RELATIONSHIP_LISTING_CACHE[next(iter(RELATIONSHIP_LISTING_CACHE))]
        
        for waiter in waiters:
            waiter.set_result_if_pending(relationship_listing)
        
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
    relationship_listing : ``None | list<Relationship>``
    """
    success, relationship_listing = _get_relationship_listing_from_cache(user_id)
    if success:
        return relationship_listing
    
    waiter = _get_relationship_listing_get_waiter(user_id)
    if (waiter is None):
        waiter = _get_relationship_listing_create_waiter(user_id)
    
    return await waiter


def _relationship_listings_query_done_callback(items, task):
    """
    Added as a callback of a query to set the result into the waiters and caches the result.
    
    Parameters
    ----------
    items : ``list<(int, list<Future>)>``
        User identifier, waiters pair.
    
    task : ``Future``
        The ran task.
    """
    try:
        relationship_listings = task.get_result()
    except BaseException as exception:
        for user_id, waiters in items:
            for waiter in waiters:
                waiter.set_exception_if_pending(exception)
    
    else:
        for user_id, waiters in items:
            relationship_listing = relationship_listings[user_id]
            
            for waiter in waiters:
                waiter.set_result_if_pending(relationship_listing)
            
            RELATIONSHIP_LISTING_CACHE[user_id] = relationship_listing
        
        while len(RELATIONSHIP_LISTING_CACHE) > RELATIONSHIP_LISTING_CACHE_SIZE_MAX:
            del RELATIONSHIP_LISTING_CACHE[next(iter(RELATIONSHIP_LISTING_CACHE))]
        
    finally:
        for user_id, waiter in items:
            del RELATIONSHIP_LISTING_GET_QUERY_TASKS[user_id]


async def get_relationship_listings(user_ids):
    """
    Gets the users' relationships.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `iterable<int>`
        User identifiers.
    
    Returns
    -------
    relationship_listings : ``dict<int, None | list<RelationShip>>``
    """
    relationship_listings = {}
    waiters = None
    user_ids_to_request = None
    
    for user_id in user_ids:
        success, relationship_listing = _get_relationship_listing_from_cache(user_id)
        if success:
            relationship_listings[user_id] = relationship_listing
            continue
        
        # get waiter if available
        waiter = _get_relationship_listing_get_waiter(user_id)
        if (waiter is not None):
            if waiters is None:
                waiters = {}
            waiters[waiter] = user_id
            continue
        
        # no waiter available, store for later.
        if user_ids_to_request is None:
            user_ids_to_request = []
            
        user_ids_to_request.append(user_id)
        continue
    
    if (user_ids_to_request is not None):
        if waiters is None:
            waiters = {}
         
        waiters.update(_get_relationship_listing_create_waiters(user_ids_to_request))
    
    if (waiters is not None):
        task_group = TaskGroup(EVENT_LOOP, waiters.keys())
        with task_group.cancel_on_exception():
            async for waiter in task_group.exhaust():
                relationship_listings[waiters[waiter]] = waiter.get_result()
    
    return relationship_listings


def _get_relationship_listing_from_cache(user_id):
    """
    Gets the user's relationships from cache.
    
    This function is a generator.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    success_and_relationship_listing : ``(bool, None | list<Relationship>)``
    """
    try:
        relationship_listing = RELATIONSHIP_LISTING_CACHE[user_id]
    except KeyError:
        return False, None
    
    RELATIONSHIP_LISTING_CACHE.move_to_end(user_id)
    return True, relationship_listing


def _get_relationship_listing_get_waiter(user_id):
    """
    Gets a waiter to request the relationships of the user. If there is no get task, returns `None`.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    waiter : ``None | Future``
    """
    try:
        task, waiters = RELATIONSHIP_LISTING_GET_QUERY_TASKS[user_id]
    except KeyError:
        return None
    
    waiter = Future(EVENT_LOOP)
    waiters.append(waiter)
    return waiter


def _get_relationship_listing_create_waiter(user_id):
    """
    Creates a waiter to request relationships of the user.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    waiter : ``Future``
    """
    waiters = []
    task = Task(EVENT_LOOP, query_relationship_listing(user_id))
    task.add_done_callback(partial_func(_relationship_listing_query_done_callback, user_id, waiters))
    RELATIONSHIP_LISTING_GET_QUERY_TASKS[user_id] = (task, waiters)
    
    waiter = Future(EVENT_LOOP)
    waiters.append(waiter)
    return waiter


def _get_relationship_listing_create_waiters(user_ids):
    """
    Creates a waiter to request relationships of the users.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user_ids : `list<int>`
        User's identifiers.
    
    Yields
    ------
    waiter_and_user_id : ``(Future, int)``
    """
    items = [(user_id, []) for user_id in user_ids]
    task = Task(EVENT_LOOP, query_relationship_listings(user_ids))
    task.add_done_callback(partial_func(_relationship_listings_query_done_callback, items))
    
    for user_id, waiters in items:
        RELATIONSHIP_LISTING_GET_QUERY_TASKS[user_id] = (task, waiters)
        waiter = Future(EVENT_LOOP)
        waiters.append(waiter)
        yield waiter, user_id


async def get_relationship_extension_traces(user_id):
    """
    Gets the user's relationships with their extensions.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifiers.
    
    Returns
    -------
    relationship_extension_traces : ``None | dict<int, RelationshipExtensionTrace>``
    """
    user_relationship_listing = await get_relationship_listing(user_id)
    if (user_relationship_listing is None):
        return None
    
    # raise RuntimeError
    relationship_extension_traces = {}
    connector_user_ids = None
    
    for relationship in user_relationship_listing:
        connector_user_id = relationship.source_user_id
        relationship_type = relationship.relationship_type
        if connector_user_id == user_id:
            connector_user_id = relationship.target_user_id
            relationship_type = do_relationship_type_flip_basic(relationship_type)
        
        # Some relationship types, like unset are not extendable, do not add them.
        if relationship_type & RELATIONSHIP_TYPES_EXTENDABLE:
            if connector_user_ids is None:
                connector_user_ids = []
            
            connector_user_ids.append(connector_user_id)
        
        relationship_extension_traces[connector_user_id] = RelationshipExtensionTrace(
            connector_user_id,
            relationship_type,
            (relationship,),
        )
    
    if (connector_user_ids is None):
        return relationship_extension_traces
    
    relationship_listings = await get_relationship_listings(connector_user_ids)
    
    for connector_user_id, relationship_listing in relationship_listings.items():
        if (relationship_listing is None) or (len(relationship_listing) == 1):
            continue
        
        connector_relationship_extension_trace = relationship_extension_traces[connector_user_id]
        connector_relationship_type = connector_relationship_extension_trace.relationship_type
        
        for relationship in relationship_listing:
            connected_id = relationship.source_user_id
            connected_relationship_type = relationship.relationship_type
            if connected_id == connector_user_id:
                connected_id = relationship.target_user_id
                connected_relationship_type = do_relationship_type_flip_basic(connected_relationship_type)
            
            # If we are back referencing, we can skip it. Trust me, I am an engineer. 
            if user_id == connected_id:
                continue
            
            try:
                connected_relationship_extension_trace = relationship_extension_traces[connected_id]
            except KeyError:
                connected_relationship_extension_trace = None
                connected_final_relationship_type = 0
            else:
                connected_final_relationship_type = connected_relationship_extension_trace.relationship_type
            
            for connection_source_relationship_type, extensions in RELATION_TYPE_EXTENSIONS:
                if not (connection_source_relationship_type & connector_relationship_type):
                    continue
                
                for connection_target_relationship_type, applier in extensions:
                    if not (connection_target_relationship_type & connected_relationship_type):
                        continue
                    
                    connected_final_relationship_type = applier(connected_final_relationship_type)
                    continue
            
            if not connected_final_relationship_type:
                continue
            
            if (connected_relationship_extension_trace is not None):
                connected_relationship_extension_trace.relationship_type = connected_final_relationship_type
            else:
                connected_relationship_extension_trace = RelationshipExtensionTrace(
                    connected_id,
                    connected_final_relationship_type,
                    (*connector_relationship_extension_trace.relationship_route, relationship),
                )
                relationship_extension_traces[connected_id] = connected_relationship_extension_trace
            continue
    
    # resolve relative sisterships
    for relationship_extension_trace in relationship_extension_traces.values():
        relationship_type = relationship_extension_trace.relationship_type
        if not (relationship_type & RELATIONSHIP_TYPE_SISTER_RELATIVE):
            continue
        
        relationship_type ^= RELATIONSHIP_TYPE_SISTER_RELATIVE
        relationship_type |= determine_relative_sister(user_id, relationship_extension_trace.user_id)
        relationship_extension_trace.relationship_type = relationship_type
    
    return relationship_extension_traces


async def query_relationship_listing(user_id):
    """
    Queries the user's relationships.
    
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
        if not results:
            relationship_listing = None
        
        else:
            relationship_listing = []
            
            for result in results:
                entry_id = result['id']
                try:
                    relationship = RELATIONSHIP_CACHE[entry_id]
                except KeyError:
                    relationship = Relationship.from_entry(result)
                    RELATIONSHIP_CACHE[entry_id] = relationship
                
                relationship_listing.append(relationship)
    
    return relationship_listing


if DB_ENGINE is None:
    @copy_docs(query_relationship_listing)
    async def query_relationship_listing(user_id):
        return None


async def query_relationship_listings(user_ids):
    """
    Queries the users' relationships.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        Users' identifiers.
    
    Returns
    -------
    relationship_listings : ``dict<int, None | list<Relationship>>``
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            RELATIONSHIP_TABLE.select().where(
                or_(
                    relationship_model.source_user_id.in_(user_ids),
                    relationship_model.target_user_id.in_(user_ids),
                ),  
            ),
        )
        
        results = await response.fetchall()
        
        relationship_listings = {user_id: None for user_id in user_ids}
        
        for result in results:
            entry_id = result['id']
            try:
                relationship = RELATIONSHIP_CACHE[entry_id]
            except KeyError:
                relationship = Relationship.from_entry(result)
                RELATIONSHIP_CACHE[entry_id] = relationship
            
            for user_id in (relationship.source_user_id, relationship.target_user_id):
                try:
                    relationship_listing = relationship_listings[user_id]
                except KeyError:
                    continue
                
                if relationship_listing is None:
                    relationship_listing = []
                    relationship_listings[user_id] = relationship_listing
                
                relationship_listing.append(relationship)
                continue
    
    return relationship_listings


if DB_ENGINE is None:
    @copy_docs(query_relationship_listings)
    async def query_relationship_listings(user_ids):
        return {user_id: None for user_id in user_ids}



async def save_relationship(relationship):
    """
    Saves the user stats.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship : ``Relationship``
        Relationship to save.
    """
    key = (relationship.source_user_id, relationship.target_user_id)
    
    try:
        task = RELATIONSHIP_SAVE_TASKS[key]
    except KeyError:
        RELATIONSHIP_SAVE_TASKS[key] = task = Task(
            EVENT_LOOP, query_save_relationship_loop(relationship)
        )
    
    await shield(task, EVENT_LOOP)


async def query_save_relationship_loop(relationship):
    """
    Runs the entry proxy saver.
    
    This method is a coroutine.
    
    Parameters
    ----------
    relationship : ``Relationship``
        Relationship to save.
    """
    try:
        async with DB_ENGINE.connect() as connector:
            entry_id = relationship.entry_id
            # If the entry is new, insert it.
            if (entry_id == 0):
                relationship.modified_fields = None
                response = await connector.execute(
                    RELATIONSHIP_TABLE.insert().values(
                        relationship_type = relationship.relationship_type,
                        source_can_boost_at = relationship.source_can_boost_at,
                        source_investment = relationship.source_investment,
                        source_user_id = relationship.source_user_id,
                        target_can_boost_at = relationship.target_can_boost_at,
                        target_investment = relationship.target_investment,
                        target_user_id = relationship.target_user_id,
                    ).returning(
                        relationship_model.id,
                    )
                )
                
                result = await response.fetchone()
                relationship.entry_id = result[0]
                _insert_relationship_to_cache(relationship)
            
            modified_fields = relationship.modified_fields
            while (modified_fields is not None):
                relationship.modified_fields = None
                
                await connector.execute(
                    RELATIONSHIP_TABLE.update(
                        relationship_model.id == entry_id,
                    ).values(
                        **modified_fields
                    )
                )
                modified_fields = relationship.modified_fields
                continue
        
    finally:
        try:
            del RELATIONSHIP_SAVE_TASKS[relationship.source_user_id, relationship.target_user_id]
        except KeyError:
            pass


if (DB_ENGINE is None):
    @copy_docs(query_save_relationship_loop)
    async def query_save_relationship_loop(relationship):
        try:
            relationship.modified_fields = None
            if not relationship.entry_id:
                relationship.entry_id = next(COUNTER)
                _insert_relationship_to_cache(relationship)
        finally:
            try:
                del RELATIONSHIP_SAVE_TASKS[relationship.source_user_id, relationship.target_user_id]
            except KeyError:
                pass


def _insert_relationship_to_cache(relationship):
    """
    Inserts the relationship to the cache.
    
    Parameters
    ----------
    relationship : ``Relationship``
        The relationship to insert.
    """
    RELATIONSHIP_CACHE[relationship.entry_id] = relationship
    
    for listing_key in (relationship.source_user_id, relationship.target_user_id):
        try:
            listing = RELATIONSHIP_LISTING_CACHE[listing_key]
        except KeyError:
            if (DB_ENGINE is not None):
                continue
            
            listing = None
        
        if (listing is None):
            RELATIONSHIP_LISTING_CACHE[listing_key] = [relationship]
            continue
        
        if (relationship not in listing):
            listing.append(relationship)
        
        continue


async def delete_relationship(relationship):
    """
    Deletes the relationship from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship : ``Relationship``
        The relationship to delete.
    """
    if not relationship.entry_id:
        return
    
    await query_delete_relationship(relationship)

    try:
        del RELATIONSHIP_CACHE[relationship.entry_id]
    except KeyError:
        pass
    
    for listing_key in (relationship.source_user_id, relationship.target_user_id):
        try:
            listing = RELATIONSHIP_LISTING_CACHE[listing_key]
        except KeyError:
            continue
        
        if (listing is None):
            continue
        
        try:
            listing.remove(relationship)
        except ValueError:
            continue
        
        if listing:
            continue
        
        RELATIONSHIP_LISTING_CACHE[listing_key] = None
        continue


async def query_delete_relationship(relationship):
    """
    Executes a query to delete the relationship from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship : ``Relationship``
        The relationship to delete.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            RELATIONSHIP_TABLE.delete().where(
                relationship_model.id == relationship.entry_id
            ),
        )


if (DB_ENGINE is None):
    @copy_docs(query_delete_relationship)
    async def query_delete_relationship(relationship):
        pass
