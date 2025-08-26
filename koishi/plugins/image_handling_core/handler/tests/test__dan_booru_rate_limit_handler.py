import vampytest

from scarletio import Task, TaskGroup, get_event_loop, sleep

from ..dan_booru import RATE_LIMIT_CONCURRENCY, RATE_LIMIT_HANDLERS, RATE_LIMIT_QUEUE, dan_booru_rate_limit_handler


async def _test_task(patched_handler, identifier):
    vampytest.assert_true(len(RATE_LIMIT_HANDLERS) <= RATE_LIMIT_CONCURRENCY)
    async for _ in patched_handler():
        vampytest.assert_true(len(RATE_LIMIT_HANDLERS) <= RATE_LIMIT_CONCURRENCY)
        
    vampytest.assert_true(len(RATE_LIMIT_HANDLERS) <= RATE_LIMIT_CONCURRENCY)
    return identifier


async def test__dan_booru_rate_limit_handler():
    """
    Tests whether ``dan_booru_rate_limit_handler`` works as intended.
    
    This function is a coroutine.
    """
    rate_limit_interval = 0.0001
    loop = get_event_loop()
    
    patched_handler = vampytest.mock_globals(
        dan_booru_rate_limit_handler,
        RATE_LIMIT_INTERVAL = rate_limit_interval,
    )
    
    task_group = TaskGroup(
        loop,
        [
            Task(loop, _test_task(patched_handler, identifier))
            for identifier in range(21)
        ],
    )
    
    response_identifiers = set()
    
    try:
        async for task in task_group.exhaust():
            response_identifiers.add(task.get_result())
    except:
        task_group.cancel_all()
        raise
    
    vampytest.assert_eq(response_identifiers, {*range(21)})
    vampytest.assert_false(RATE_LIMIT_QUEUE)    
    await sleep(rate_limit_interval, loop)
    vampytest.assert_not(RATE_LIMIT_HANDLERS)
