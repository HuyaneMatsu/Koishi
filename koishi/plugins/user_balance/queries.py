__all__ = ('get_user_balance', 'get_user_balances')

from hata import KOKORO
from scarletio import Future, Task, TaskGroup, copy_docs

from ...bot_utils.models import DB_ENGINE, USER_BALANCE_TABLE, user_balance_model

from .constants import USER_BALANCE_CACHE, USER_BALANCE_QUERY_TASKS
from .user_balance import UserBalance


async def get_user_balance(user_id):
    """
    Gets the balance of the given user for their identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User identifier.
    
    Returns
    -------
    user_balance : ``UserBalance``
    """
    user_balance = _get_user_balance_from_cache(user_id)
    if (user_balance is not None):
        return user_balance
    
    return (await _get_user_balance_query_waiter(user_id))


async def get_user_balances(user_ids):
    """
    Gets the balance of the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `iterable<int>`
        User identifiers.
    
    Returns
    -------
    user_balances : `dict<int, UserBalance>`
    """
    user_balances = {}
    waiters = None
    
    for user_id in user_ids:
        user_balance = _get_user_balance_from_cache(user_id)
        if (user_balance is not None):
            user_balances[user_id] = user_balance
            continue
        
        waiter = _get_user_balance_query_waiter(user_id)
        if waiters is None:
            waiters = []
        
        waiters.append(waiter)
        continue
    
    if (waiters is not None):
        task_group = TaskGroup(KOKORO, waiters)
        with task_group.cancel_on_exception():
            async for waiter in task_group.exhaust():
                user_balance = waiter.get_result()
                user_balances[user_balance.user_id] = user_balance
    
    return user_balances


def _get_user_balance_from_cache(user_id):
    """
    Gets the user balance from cache.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to get the balance for.
    
    Returns
    -------
    user_balance : `None | UserBalance`
    """
    try:
        user_balance = USER_BALANCE_CACHE[user_id]
    except KeyError:
        return None
    
    USER_BALANCE_CACHE.move_to_end(user_id)
    return user_balance


def _get_user_balance_query_waiter(user_id):
    """
    Returns a user balance waiter.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to get the balance for.
    
    Returns
    -------
    waiter : ``Future``
    """
    try:
        task, waiters = USER_BALANCE_QUERY_TASKS[user_id]
    except KeyError:
        waiters = []
        task = Task(KOKORO, query_user_balance(user_id, waiters))
        USER_BALANCE_QUERY_TASKS[user_id] = (task, waiters)
    
    waiter = Future(KOKORO)
    waiters.append(waiter)
    return waiter


async def query_user_balance(user_id, waiters):
    """
    Requests the to do entries from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier to query for.
    
    waiters : `list<Future>`
        Result waiters.
    """
    try:
        async with DB_ENGINE.connect() as connector:
            response = await connector.execute(
                USER_BALANCE_TABLE.select().where(
                    user_balance_model.user_id == user_id,
                ),
            )
            
            result = await response.fetchone()
            if result is None:
                user_balance = UserBalance(user_id)
            else:
                user_balance = UserBalance.from_entry(result)
        
    except BaseException as exception:
        for waiter in waiters:
            waiter.set_exception_if_pending(exception)
        raise
    
    else:
        for waiter in waiters:
            waiter.set_result_if_pending(user_balance)
    
    finally:
        try:
            del USER_BALANCE_QUERY_TASKS[user_id]
        except KeyError:
            pass


if (DB_ENGINE is None):
    @copy_docs(query_user_balance)
    async def query_user_balance(user_id, waiters):
        try:
            user_balance = UserBalance(user_id)
            
            for waiter in waiters:
                waiter.set_result_if_pending(user_balance)
        
        finally:
            try:
                del USER_BALANCE_QUERY_TASKS[user_id]
            except KeyError:
                pass
