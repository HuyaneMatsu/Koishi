__all__ = ()

from ...bots import MAIN_CLIENT

from .looping import start_looping, stop_looping


def setup(module):
    """
    Called after the module is loaded. Starts looping if the client is running.
    
    Parameters
    ----------
    module : ``ModuleType``
        This module.
    """
    if MAIN_CLIENT.running:
        start_looping()


async def teardown(module):
    """
    Called after the module is unloaded. Stops looping.
    
    This function is a coroutine.
    
    Parameters
    ----------
    module : ``ModuleType``
        This module.
    """
    await stop_looping()


@MAIN_CLIENT.events
async def ready(client):
    """
    Handles a ready event. Starts looping.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    """
    client.events.remove(ready)
    start_looping()


@MAIN_CLIENT.events
async def shutdown(client):
    """
    Handles a shutdown event. Stops looping.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    """
    MAIN_CLIENT.events(ready)
    await stop_looping()
