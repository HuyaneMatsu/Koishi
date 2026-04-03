from collections import OrderedDict
from types import FunctionType

import vampytest
from scarletio import Task, get_event_loop

from ..constants import STATISTIC_CACHE_TIMEOUT
from ..statistic_caching_and_synchronization import QueryCacherAndSynchronizer


def _assert_fields_set(query_cacher_and_synchronizer):
    """
    Asserts whether all the fields of the given instance are set.
    
    Parameters
    ----------
    query_cacher_and_synchronizer : ``QueryCacherAndSynchronizer``
        The instance to check.
    """
    vampytest.assert_instance(query_cacher_and_synchronizer, QueryCacherAndSynchronizer)
    vampytest.assert_instance(query_cacher_and_synchronizer.coroutine_function, FunctionType)
    

def test__QueryCacherAndSynchronizer__new():
    """
    Tests whether ``QueryCacherAndSynchronizer.__new__`` works as intended.
    """
    async def coroutine_function(page_size):
        pass
    
    query_cacher_and_synchronizer = QueryCacherAndSynchronizer(coroutine_function)
    _assert_fields_set(query_cacher_and_synchronizer)
    
    vampytest.assert_is(query_cacher_and_synchronizer.coroutine_function, coroutine_function)
    

async def test__QueryCacherAndSynchronizer__call__new():
    """
    Tests whether ``QueryCacherAndSynchronizer.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: new.
    """
    page_size = 20
    coroutine_function_called = 0
    monotonic_time = 1.1
    
    result_0 = [
        (56, 12),
        (57, 10),
    ]
    
    def monotonic():
        nonlocal monotonic_time
        return monotonic_time
    
    statistics_cache = OrderedDict()
    
    
    async def coroutine_function(input_page_size):
        nonlocal page_size
        nonlocal coroutine_function_called
        nonlocal result_0
        
        vampytest.assert_eq(page_size, input_page_size)
        coroutine_function_called = True
        return result_0
    
    
    mocked = vampytest.mock_globals(
        QueryCacherAndSynchronizer.__call__,
        2,
        monotonic = monotonic,
        STATISTIC_CACHE = statistics_cache,
    )
    
    
    query_cacher_and_synchronizer = QueryCacherAndSynchronizer(coroutine_function)
    
    task = Task(get_event_loop(), mocked(query_cacher_and_synchronizer, page_size))
    task.apply_timeout(0.001)
    output = await task
    
    vampytest.assert_eq(
        output,
        result_0,
    )
    
    vampytest.assert_eq(
        [*statistics_cache.items()],
        [
            ((coroutine_function, (page_size, )), (STATISTIC_CACHE_TIMEOUT + monotonic_time, result_0))
        ],
    )
    
    vampytest.assert_true(coroutine_function_called)


async def test__QueryCacherAndSynchronizer__call__overwrite():
    """
    Tests whether ``QueryCacherAndSynchronizer.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: overwrite.
    """
    page_size = 20
    coroutine_function_called = 0
    monotonic_time = STATISTIC_CACHE_TIMEOUT + 100.1
    
    result_0 = [
        (56, 12),
        (57, 10),
    ]
    
    result_1 = [
        (56, 13),
        (57, 19),
    ]
    
    def monotonic():
        nonlocal monotonic_time
        return monotonic_time
    
    statistics_cache = OrderedDict()
    
    
    async def coroutine_function(input_page_size):
        nonlocal page_size
        nonlocal coroutine_function_called
        nonlocal result_1
        
        vampytest.assert_eq(page_size, input_page_size)
        coroutine_function_called = True
        return result_1
    
    
    mocked = vampytest.mock_globals(
        QueryCacherAndSynchronizer.__call__,
        2,
        monotonic = monotonic,
        STATISTIC_CACHE = statistics_cache,
    )
    
    statistics_cache[coroutine_function, (page_size, )] = (56.12, result_0)
    
    query_cacher_and_synchronizer = QueryCacherAndSynchronizer(coroutine_function)
    
    task = Task(get_event_loop(), mocked(query_cacher_and_synchronizer, page_size))
    task.apply_timeout(0.001)
    output = await task
    
    vampytest.assert_eq(
        output,
        result_1,
    )
    
    vampytest.assert_eq(
        [*statistics_cache.items()],
        [
            ((coroutine_function, (page_size, )), (STATISTIC_CACHE_TIMEOUT + monotonic_time, result_1))
        ],
    )
    
    vampytest.assert_true(coroutine_function_called)


async def test__QueryCacherAndSynchronizer__call__keep():
    """
    Tests whether ``QueryCacherAndSynchronizer.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: keep.
    """
    page_size = 20
    coroutine_function_called = 0
    monotonic_time = 1.1
    
    result_0 = [
        (56, 12),
        (57, 10),
    ]
    
    result_1 = [
        (56, 13),
        (57, 19),
    ]
    
    def monotonic():
        nonlocal monotonic_time
        return monotonic_time
    
    statistics_cache = OrderedDict()
    
    
    async def coroutine_function(input_page_size):
        nonlocal page_size
        nonlocal coroutine_function_called
        nonlocal result_1
        
        vampytest.assert_eq(page_size, input_page_size)
        coroutine_function_called = True
        return result_1
    
    
    mocked = vampytest.mock_globals(
        QueryCacherAndSynchronizer.__call__,
        2,
        monotonic = monotonic,
        STATISTIC_CACHE = statistics_cache,
    )
    
    statistics_cache[coroutine_function, (page_size, )] = (STATISTIC_CACHE_TIMEOUT + 56.12, result_0)
    
    query_cacher_and_synchronizer = QueryCacherAndSynchronizer(coroutine_function)
    
    task = Task(get_event_loop(), mocked(query_cacher_and_synchronizer, page_size))
    task.apply_timeout(0.001)
    output = await task
    
    vampytest.assert_eq(
        output,
        result_0,
    )
    
    vampytest.assert_eq(
        [*statistics_cache.items()],
        [
            ((coroutine_function, (page_size, )), (STATISTIC_CACHE_TIMEOUT + 56.12, result_0))
        ],
    )
    
    vampytest.assert_false(coroutine_function_called)
