__all__ = (
    'add_linked_quest', 'delete_linked_quest', 'get_linked_quest_listing', 'modify_linked_quest_amount_submitted'
)

from functools import partial as partial_func
from itertools import count

from scarletio import Future, Task, copy_docs, get_event_loop

from ...bot_utils.models import DB_ENGINE, LINKED_QUEST_TABLE, linked_quest_model

from .constants import (
    LINKED_QUEST_LISTING_CACHE, LINKED_QUEST_LISTING_CACHE_SIZE_MAX, LINKED_QUEST_LISTING_GET_QUERY_TASKS
)
from .linked_quest import LinkedQuest


EVENT_LOOP = get_event_loop()


async def get_linked_quest_listing(user_id):
    """
    Gets the user's linked quests.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    linked_quest_listing : ``None | list<LinkedQuest>``
    """
    try:
        quest_listing = LINKED_QUEST_LISTING_CACHE[user_id]
    except KeyError:
        pass
    else:
        LINKED_QUEST_LISTING_CACHE.move_to_end(user_id)
        return quest_listing
    
    try:
        task, waiters = LINKED_QUEST_LISTING_GET_QUERY_TASKS[user_id]
    except KeyError:
        waiters = []
        task = Task(EVENT_LOOP, query_linked_quest_listing(user_id))
        task.add_done_callback(partial_func(_linked_quest_listing_query_done_callback, user_id, waiters))
        LINKED_QUEST_LISTING_GET_QUERY_TASKS[user_id] = (task, waiters)
    
    waiter = Future(EVENT_LOOP)
    waiters.append(waiter)
    return await waiter


def _linked_quest_listing_query_done_callback(key, waiters, task):
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
        LINKED_QUEST_LISTING_CACHE[key] = listing
        if len(LINKED_QUEST_LISTING_CACHE) > LINKED_QUEST_LISTING_CACHE_SIZE_MAX:
            del LINKED_QUEST_LISTING_CACHE[next(iter(LINKED_QUEST_LISTING_CACHE))]
        
        for waiter in waiters:
            waiter.set_result_if_pending(listing)
        
    finally:
        del LINKED_QUEST_LISTING_GET_QUERY_TASKS[key]


async def query_linked_quest_listing(user_id):
    """
    Queries the user's linked quests.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    linked_quest_listing : ``None | list<LinkedQuest>``
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            LINKED_QUEST_TABLE.select().where(
                linked_quest_model.user_id == user_id,
            ),
        )
        
        results = await response.fetchall()
        if results:
            linked_quests = [LinkedQuest.from_entry(result) for result in results]
        else:
            linked_quests = None
    
    return linked_quests


if DB_ENGINE is None:
    @copy_docs(query_linked_quest_listing)
    async def query_linked_quest_listing(user_id):
        return None


async def delete_linked_quest(linked_quest):
    """
    Deletes the given linked quest.
    
    This function is a coroutine.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to delete.
    """
    user_id = linked_quest.user_id
    try:
        quest_listing = LINKED_QUEST_LISTING_CACHE[user_id]
    except KeyError:
        pass
    else:
        LINKED_QUEST_LISTING_CACHE.move_to_end(user_id)
        
        if (quest_listing is not None):
            try:
                quest_listing.remove(linked_quest)
            except ValueError:
                pass
            else:
                if not quest_listing:
                    LINKED_QUEST_LISTING_CACHE[user_id] = None
    
    
    await query_delete_linked_quest(linked_quest.entry_id)


async def query_delete_linked_quest(entry_id):
    """
    Deletes the linked quest from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry_id : `int`
        The entry's identifier to delete.
    """
    if entry_id == -1:
        return
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            LINKED_QUEST_TABLE.delete().where(
                linked_quest_model.id == entry_id,
            ),
        )

if DB_ENGINE is None:
    @copy_docs(query_delete_linked_quest)
    async def query_delete_linked_quest(entry_id):
        return


async def add_linked_quest(linked_quest):
    """
    Adds the linked quest with the given.
    
    This function is a coroutine.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to add.
    """
    user_id = linked_quest.user_id
    try:
        quest_listing = LINKED_QUEST_LISTING_CACHE[user_id]
    except KeyError:
        pass
    else:
        LINKED_QUEST_LISTING_CACHE.move_to_end(user_id)
        
        if (quest_listing is None):
            quest_listing = [linked_quest]
            LINKED_QUEST_LISTING_CACHE[user_id] = quest_listing
        else:
            quest_listing.append(linked_quest)
    
    entry_id = await query_add_linked_quest(linked_quest)
    linked_quest.entry_id = entry_id


async def query_add_linked_quest(linked_quest):
    """
    Adds the linked quest to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to add.
    
    Returns
    -------
    entry_id : `int`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            LINKED_QUEST_TABLE.insert().values(
                amount_required = linked_quest.amount_required,
                amount_submitted = linked_quest.amount_submitted,
                batch_id = linked_quest.batch_id,
                expires_at = linked_quest.expires_at,
                guild_id = linked_quest.guild_id,
                reward_balance = linked_quest.reward_balance,
                reward_credibility = linked_quest.reward_credibility,
                taken_at = linked_quest.taken_at,
                template_id = linked_quest.template_id,
                user_id = linked_quest.user_id,
            ).returning(
                linked_quest_model.id,
            )
        )
        
        result = await response.fetchone()
        return result[0]


if DB_ENGINE is None:
    LINKED_QUEST_ID_GENERATOR = iter(count(1))
    
    @copy_docs(query_add_linked_quest)
    async def query_add_linked_quest(linked_quest):
        return next(LINKED_QUEST_ID_GENERATOR)


async def modify_linked_quest_amount_submitted(linked_quest, amount):
    """
    Modifies the linked quest's submitted amount.
    
    This function is a coroutine.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to modify.
    
    amount : `int`
        The new submitted amount of the quest.
    """
    try:
        await query_modify_lined_quest_amount_submitted(linked_quest.entry_id, amount)
    finally:
        linked_quest.amount_submitted = amount


async def query_modify_lined_quest_amount_submitted(entry_id, amount):
    """
    Modifies the entry for the given identifier in the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry_id : `int`
        The entry's identifier.
    
    amount : `int`
        New amount to set.
    """
    if entry_id == -1:
        return
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            LINKED_QUEST_TABLE.update(
                linked_quest_model.id == entry_id
            ).values(
                amount_submitted = amount,
            )
        )


if DB_ENGINE is None:
    @copy_docs(query_modify_lined_quest_amount_submitted)
    async def query_modify_lined_quest_amount_submitted(entry_id, amount):
        return
