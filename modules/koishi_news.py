__all__ = ()

from bot_utils.constants import CHANNEL__SUPPORT__KOISHI_NEWS
from bots import Satori


async def crosspost_message(client, message):
    """
    Crossposts a created koishi news message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the message.
    message : ``Message``
        The created message.
    """
    await client.message_crosspost(message)


def setup(module):
    """
    Called after the plugin is loaded.
    
    Parameters
    ----------
    module : `ModuleType`
    """
    Satori.events.message_create.append(CHANNEL__SUPPORT__KOISHI_NEWS, crosspost_message)


def teardown(module):
    """
    Called before the plugin is unloaded.
    
    Parameters
    ----------
    module : `ModuleType`
    """
    Satori.events.message_create.remove(CHANNEL__SUPPORT__KOISHI_NEWS, crosspost_message)
