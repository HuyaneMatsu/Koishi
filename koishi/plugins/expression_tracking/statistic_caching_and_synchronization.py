__all__ = ()

from functools import partial as partial_func
from time import monotonic

from scarletio import Future, RichAttributeErrorBaseType, Task, get_event_loop

from .constants import STATISTIC_CACHE, STATISTIC_CACHE_SIZE_MAX, STATISTIC_CACHE_TIMEOUT, STATISTIC_QUERY_TASKS


EVENT_LOOP = get_event_loop()


def _get_from_cache(key):
    """
    Tries to get the result from cache.
    
    Parameters
    ----------
    key : `(CoroutineFunction, tuple<object>)`
        Key used in caching. First element is the coroutine function to run and the second are the parameters.
    
    Returns
    -------
    entries : `None | list<RowProxy<int, int>>`
    """
    try:
        timeout, entries = STATISTIC_CACHE[key]
    except KeyError:
        return
    
    if timeout < monotonic():
        STATISTIC_CACHE.move_to_end(key)
        return entries
    
    try:
        del STATISTIC_CACHE[key]
    except KeyError:
        pass


def _query_done_callback(key, waiters, task):
    """
    Added as a callback of a query to set the result into the waiters and caches the result.
    
    Parameters
    ----------
    key : `(CoroutineFunction, tuple<object>)`
        Key used in caching. First element is the coroutine function to run and the second are the parameters.
    
    waiters : `list<Future>`
        Result waiters.
    
    task : ``Future``
        The ran task.
    """
    try:
        entries = task.get_result()
    except BaseException as exception:
        for waiter in waiters:
            waiter.set_exception_if_pending(exception)
    else:
        STATISTIC_CACHE[key] = (monotonic() + STATISTIC_CACHE_TIMEOUT, entries)
        if len(STATISTIC_CACHE) == STATISTIC_CACHE_SIZE_MAX:
            del STATISTIC_CACHE[next(iter(STATISTIC_CACHE))]
        
        for waiter in waiters:
            waiter.set_result_if_pending(entries)
        
    finally:
        del STATISTIC_QUERY_TASKS[key]


class QueryCacherAndSynchronizer(RichAttributeErrorBaseType):
    """
    Caches the results of the queries and synchronizes their runs.
    
    Attributes
    ----------
    coroutine_function : `CoroutineFunction`
        The wrapped function.
    """
    __slots__ = ('coroutine_function',)
    
    
    def __new__(cls, coroutine_function):
        """
        Creates a new query cacher and synchronizer.
        
        Parameters
        ----------
        coroutine_function : `CoroutineFunction`
            The function to wrap.
        """
        self = object.__new__(cls)
        self.coroutine_function = coroutine_function
        return self
        
    
    async def __call__(self, *positional_parameters):
        """
        Returns the result if cached, if not requests it in a synchronized manner.
        
        This function is a coroutine.
        
        Parameters
        ----------
        *positional_parameters : Positional parameters
            Positional parameters to call the wrapped `coroutine_function` with.
        
        Returns
        -------
        entries : `list<RowProxy<int, int>>`
        """
        coroutine_function = self.coroutine_function
        key = (coroutine_function, positional_parameters)
        
        entries = _get_from_cache(key)
        if (entries is not None):
            return entries
        
        try:
            task, waiters = STATISTIC_QUERY_TASKS[key]
        except KeyError:
            waiters = []
            task = Task(EVENT_LOOP, coroutine_function(*positional_parameters))
            task.add_done_callback(partial_func(_query_done_callback, key, waiters))
            STATISTIC_QUERY_TASKS[key] = (task, waiters)
        
        waiter = Future(EVENT_LOOP)
        waiters.append(waiter)
        return await waiter
