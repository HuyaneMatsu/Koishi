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
    
    waiter = _get_user_balance_query_waiter(user_id)
    if waiter is None:
        waiter = _create_user_balance_query_waiter(user_id)
    
    return (await waiter)


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
    user_ids_to_request = None
    
    for user_id in user_ids:
        user_balance = _get_user_balance_from_cache(user_id)
        if (user_balance is not None):
            user_balances[user_id] = user_balance
            continue
        
        # get waiter if available
        waiter = _get_user_balance_query_waiter(user_id)
        if (waiter is not None):
            if waiters is None:
                waiters = []
            waiters.append(waiter)
        
        # no waiter available, store for later.
        if user_ids_to_request is None:
            user_ids_to_request = []
        
        user_ids_to_request.append(user_id)
        continue
    
    if (user_ids_to_request is not None):
        if waiters is None:
            waiters = []
        
        waiters.extend(_create_user_balance_query_waiters(user_ids_to_request))
    
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
    Returns a user balance waiter. If there is no waiter yet, returns `None`.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to get the balance for.
    
    Returns
    -------
    waiter : `None | Future`
    """
    try:
        task, waiters = USER_BALANCE_QUERY_TASKS[user_id]
    except KeyError:
        return None
    
    waiter = Future(KOKORO)
    waiters.append(waiter)
    return waiter


def _create_user_balance_query_waiter(user_id):
    """
    Creates a user balance query waiter. Use it after `_get_user_balance_query_waiter`.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to get the balance for.
    
    Returns
    -------
    waiter : `Future`
    """
    waiters = []
    task = Task(KOKORO, query_user_balance(user_id, waiters))
    USER_BALANCE_QUERY_TASKS[user_id] = (task, waiters)
    waiter = Future(KOKORO)
    waiters.append(waiter)
    return waiter


def _create_user_balance_query_waiters(user_ids):
    """
    Creates user balance query waiters.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user_ids : `list<int>`
        User identifier to get the balance for.
    
    Yields
    ------
    waiter : `Future`
    """
    items = [(user_id, []) for user_id in user_ids]
    task = Task(KOKORO, query_user_balances(items))
    
    for user_id, waiters in items:
        USER_BALANCE_QUERY_TASKS[user_id] = (task, waiters)
        waiter = Future(KOKORO)
        waiters.append(waiter)
        yield waiter


async def query_user_balance(user_id, waiters):
    """
    Requests the to user balance entries from the database.
    
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


async def query_user_balances(items):
    """
    Requests the user balance entries from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    items : `list<(int, list<Future>>`
        A list of user's identifier and result waiter pairs.
    """
    try:
        async with DB_ENGINE.connect() as connector:
            response = await connector.execute(
                USER_BALANCE_TABLE.select().where(
                    user_balance_model.user_id.in_([item[0] for item in items]),
                ),
            )
            
            results = await response.fetchall()
            
            user_balances = {}
            
            for result in results:
                user_balance = UserBalance.from_entry(result)
                user_balances[user_balance.user_id] = user_balance
    
    except BaseException as exception:
        for item in items:
            waiters = item[1]
            for waiter in waiters:
                waiter.set_exception_if_pending(exception)
        raise
    
    else:
        for user_id, waiters in items:
            try:
                user_balance = user_balances[user_id]
            except KeyError:
                user_balance = UserBalance(user_id)
            
            for waiter in waiters:
                waiter.set_result_if_pending(user_balance)
    
    finally:
        for item in items:
            user_id = item[0]
            try:
                del USER_BALANCE_QUERY_TASKS[user_id]
            except KeyError:
                pass


if (DB_ENGINE is None):
    @copy_docs(query_user_balance)
    async def query_user_balances(items):
        try:
            for user_id, waiters in items:
                user_balance = UserBalance(user_id)
                
                for waiter in waiters:
                    waiter.set_result_if_pending(user_balance)
        
        finally:
            for item in items:
                user_id = item[0]
                try:
                    del USER_BALANCE_QUERY_TASKS[user_id]
                except KeyError:
                    pass
