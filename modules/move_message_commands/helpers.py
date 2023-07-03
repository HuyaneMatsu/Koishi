__all__ = ()

from hata import DiscordException, ERROR_CODES


async def message_delete(client, message):
    """
    Deletes the given message with the client.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    message : ``Message``
        The message to delete.
    """
    try:
        await client.message_delete(message)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_message:
            return
        
        raise
    
    except ConnectionError:
        return
