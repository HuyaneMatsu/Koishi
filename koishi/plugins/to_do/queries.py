__all__ = ()

from itertools import count

from hata import KOKORO
from scarletio import Future, Task, copy_docs
from sqlalchemy.sql import select

from ...bot_utils.models import DB_ENGINE, TODO_TABLE, todo_model

from .to_do import ToDo


if DB_ENGINE is None:
    COUNTER = iter(count(1))


TO_DO_LISTING = None
TO_DO_LISTING_QUERY_WAITERS = None


async def get_to_do_listing():
    """
    Requests the to do entries. If they are already cached, returns them instead.
    
    This function is a coroutine.
    
    Returns
    -------
    to_do_listing : ``list<ToDo>``
    """
    global TO_DO_LISTING_QUERY_WAITERS
    
    if (TO_DO_LISTING is not None):
        return TO_DO_LISTING
    
    if (TO_DO_LISTING_QUERY_WAITERS is None):
        TO_DO_LISTING_QUERY_WAITERS = []
        Task(KOKORO, query_get_to_do_listing())
    
    future = Future(KOKORO)
    TO_DO_LISTING_QUERY_WAITERS.append(future)
    await future
    return TO_DO_LISTING


async def query_get_to_do_listing():
    """
    Requests the to do entries from the database.
    
    This function is a coroutine.
    """
    global TO_DO_LISTING
    global TO_DO_LISTING_QUERY_WAITERS
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    todo_model.id,
                    todo_model.name,
                    todo_model.description,
                    todo_model.created_at,
                    todo_model.creator_id,
                ]
            )
        )
        
        results = await response.fetchall()
    
    TO_DO_LISTING = [ToDo.from_entry(result) for result in results]
    for future in TO_DO_LISTING_QUERY_WAITERS:
        future.set_result_if_pending(None)
    TO_DO_LISTING_QUERY_WAITERS = None


if DB_ENGINE is None:
    @copy_docs(query_get_to_do_listing)
    async def query_get_to_do_listing():
        global TO_DO_LISTING
        global TO_DO_LISTING_QUERY_WAITERS
        
        TO_DO_LISTING = []
        for future in TO_DO_LISTING_QUERY_WAITERS:
            future.set_result_if_pending(None)


async def insert_to_do(to_do):
    """
    Inserts the to-do entry into the data base.
    
    This function is a coroutine.
    
    Parameters
    ----------
    to_do : ``ToDo``
        The to do entry to insert.
    """
    if to_do.entry_id:
        return
    
    entry_id = await query_insert_to_do(to_do)
    to_do.entry_id = entry_id
    if (TO_DO_LISTING is not None):
        TO_DO_LISTING.append(to_do)


async def query_insert_to_do(to_do):
    """
    Executes a to do entry insertion query.
    
    This function is a coroutine.
    
    Parameters
    ----------
    to_do : ``ToDo``
        The to do entry to insert.
    
    Returns
    -------
    entry_id : `int`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            TODO_TABLE.insert().values(
                created_at = to_do.created_at,
                creator_id = to_do.creator_id,
                description = to_do.description,
                name = to_do.name,
            ).returning(
                todo_model.id,
            )
        )
        result = await response.fetchone()
        return result[0]


if DB_ENGINE is None:
    @copy_docs(query_insert_to_do)
    async def query_insert_to_do(to_do):
        return next(COUNTER)


async def update_to_do(to_do):
    """
    Updates the to do entry.
    
    This function is a coroutine.
    
    Parameters
    ----------
    to_do : ``ToDo``
        The to do entry to update.
    """
    if not to_do.entry_id:
        return
    
    await query_update_to_do(to_do)


async def query_update_to_do(to_do):
    """
    Executes a query to update the to do entry in the data base.
    
    This function is a coroutine.
    
    Parameters
    ----------
    to_do : ``ToDo``
        The to do entry to update.
    """
    # Only name and description can be modified, so save only those.
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            TODO_TABLE.update(
                todo_model.id == to_do.entry_id,
            ).values(
                description = to_do.description,
                name = to_do.name,
            )
        )


if DB_ENGINE is None:
    @copy_docs(query_update_to_do)
    async def query_update_to_do(to_do):
        return


async def delete_to_do(to_do):
    """
    Deletes the to-do entry from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    to_do : ``ToDo``
        The to do entry to delete.
    """
    if not to_do.entry_id:
        return
    
    await query_delete_to_do(to_do)
    
    if (TO_DO_LISTING is not None):
        try:
            TO_DO_LISTING.remove(to_do)
        except ValueError:
            pass


async def query_delete_to_do(to_do):
    """
    Executes a query to delete teh entry from the data base.
    
    This function is a coroutine.
    
    Parameters
    ----------
    to_do : ``ToDo``
        The to do entry to delete.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            TODO_TABLE.delete().where(
                todo_model.id == to_do.entry_id,
            )
        )


if DB_ENGINE is None:
    @copy_docs(query_delete_to_do)
    async def query_delete_to_do(to_do):
        return
