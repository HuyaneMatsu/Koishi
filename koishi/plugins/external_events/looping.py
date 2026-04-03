__all__ = ()

from hata import KOKORO
from scarletio import LOOP_TIME, Task, TaskGroup, sleep

from ...bots import MAIN_CLIENT

from .handling import HANDLERS
from .queries import pull_external_events, remove_external_events


KEEP_LOOPING = False
CURRENT_STEP_TASK = None
LOOP_STEP = 10.0


async def loop_step():
    """
    Does a loop step.
    
    This function is a coroutine.
    """
    external_events = await pull_external_events()
    if external_events is None:
        return
    
    task_group = None
    
    for external_event in external_events:
        handler = HANDLERS.get(external_event.event_type, None)
        if handler is None:
            continue
        
        if task_group is None:
            task_group = TaskGroup(KOKORO)
        
        task_group.create_task(handler(external_event))
        continue
    
    if task_group is None:
        return
    
    async for task in task_group.exhaust():
        if task.is_cancelled():
            continue
        
        exception = task.get_exception()
        if (exception is None):
            continue
        
        Task(KOKORO, MAIN_CLIENT.events.error(MAIN_CLIENT, 'loop_step', exception))
        continue
    
    await remove_external_events([external_event.entry_id for external_event in external_events])


async def loop_task():
    """
    Calls ``loop_step`` while looping is allowed.
    
    This function is a coroutine.
    """
    global KEEP_LOOPING
    global CURRENT_STEP_TASK
    
    KEEP_LOOPING = True
    
    while True:
        CURRENT_STEP_TASK = Task(KOKORO, loop_step())
        try:
            await CURRENT_STEP_TASK
        finally:
            CURRENT_STEP_TASK = None
        
        before = LOOP_TIME()
        if not KEEP_LOOPING:
            break
        
        end = LOOP_TIME()
        
        await sleep(LOOP_STEP + before - end, KOKORO)
        
        if not KEEP_LOOPING:
            break


async def stop_looping():
    """
    Stops looping.
    
    This function is a coroutine.
    """
    global KEEP_LOOPING
    
    if not KEEP_LOOPING:
        return
    
    KEEP_LOOPING = False
    
    if (CURRENT_STEP_TASK is not None):
        await CURRENT_STEP_TASK


def start_looping():
    """
    Begins looping.
    """
    if KEEP_LOOPING:
        return
    
    Task(KOKORO, loop_task())
