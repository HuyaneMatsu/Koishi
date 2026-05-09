__all__ = ()

from itertools import islice

from hata import DiscordException
from scarletio import CauseGroup, copy_docs

from ...bot_utils.models import DB_ENGINE
from ...bots import MAIN_CLIENT


async def execute_remind(location, entries_getter, notifier):
    """
    Execute a remind action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    location : `str`
        Location name to use for exception handler.
    
    entries_getter : `CoroutineFunctionType`
        A function to get the entries to be reminded.
    
    notifier : `CoroutineFunctionType`
        Notifier function.
    """
    async with DB_ENGINE.connect() as connector:
        await remind_with_connector(location, entries_getter, notifier, connector)


if DB_ENGINE is None:
    @copy_docs(execute_remind)
    async def execute_remind(location, entries_getter, notifier):
        await remind_with_connector(location, entries_getter, notifier, None)


async def call_exception_handler(location, collected_exceptions):
    """
    Calls the main client's exception handlers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    location : `str`
        Location name to use for exception handler.
    
    collected_exceptions : ``list<DiscordException>``
        The collected exceptions while reminding.
    """
    try:
        exception = collected_exceptions[-1]
        collected_exception_length = len(collected_exceptions)
        if collected_exception_length > 1:
            exception.__cause__ = CauseGroup(*islice(collected_exceptions, None, collected_exception_length - 1))
        
        await MAIN_CLIENT.events.error(MAIN_CLIENT, location, exception)
        
    finally:
        collected_exceptions = None
        exception = None


async def remind_with_connector(location, entries_getter, notifier, connector):
    """
    Reminds the users who forgot to claim their daily.
    
    This function is a coroutine.
    
    Parameters
    ----------
    location : `str`
        Location name to use for exception handler.
    
    entries_getter : `CoroutineFunctionType`
        A function to get the entries to be reminded.
    
    notifier : `CoroutineFunctionType`
        Notifier function.
    
    connector : ``None | AsyncConnection``
        Database connector.
    """
    collected_exceptions = None
    
    results = await entries_getter(connector)
    for entry in results:
        try:
            await notifier(entry, connector)
        
        except DiscordException as exception:
            if collected_exceptions is None:
                collected_exceptions = []
            collected_exceptions.append(exception)
    
    if collected_exceptions is not None:
        try:
            await call_exception_handler(location, collected_exceptions)
        finally:
            collected_exceptions = None


async def request_interval(location, interval_default, interval_getter):
    """
    Requests how much time should be waited between.
    
    This function is a coroutine.
    
    Parameters
    ----------
    location : `str`
        Location name to use for exception handler.
    
    interval_default : `float`
        The amount of seconds between runs.
    
    interval_getter : `None | CoroutineFunctionType`
        Function to get the amount of time till next call.
    
    Returns
    -------
    interval : `float`
    """
    if interval_getter is None:
        interval = interval_default
    
    else:
        try:
            interval = await interval_getter(interval_default)
        except GeneratorExit:
            raise
        
        except BaseException as exception:
            await call_exception_handler(location, [exception])
            interval = interval_default
    
    return interval
