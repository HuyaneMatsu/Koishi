__all__ = ('try_channel_create', 'try_message_create', 'try_user_get')

from hata import DiscordException, ERROR_CODES

from ...bot_utils.user_getter import get_user


async def try_user_get(user_id):
    """
    Tries to get the user. On success returns it.
    If it cannot get the user sets that they were already notified to avoid repeat.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier to get.
    
    Returns
    -------
    user_and_set_as_notified : ``(None | ClientUserBase, bool)``
    """
    try:
        user = await get_user(user_id)
    except GeneratorExit:
        raise
    
    except ConnectionError:
        return None, False
    
    except DiscordException as exception:
        # server error, pretty normal at this point lol
        if exception.status >= 500:
            return None, False
        
        # user deleted
        if exception.code == ERROR_CODES.unknown_user:
            return None, True
        
        raise
    
    return user, False


async def try_channel_create(client, user_id):
    """
    Tries to create private channel with the user. On success returns it.
    If cannot create channel to the user sets that they were already notified to avoid repeat.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client to create the message with.
    
    user_id : `int`
        The user's identifier to create the channel towards.
    
    Returns
    -------
    channel_and_set_as_notified : ``(None | Channel, False)``
    """
    try:
        channel = await client.channel_private_create(user_id)
    except GeneratorExit:
        raise
    
    except ConnectionError:
        return None, False
    
    except DiscordException as exception:
        # server error, pretty normal at this point lol
        if exception.status >= 500:
            return None, False
        
        # user deleted
        if exception.code == ERROR_CODES.unknown_user:
            return None, True
        
        raise
    
    return channel, False


async def try_message_create(client, channel, components):
    """
    Tries to create the message. On success returns it.
    If the user cannot be messaged set that they were already notified to avoid repeat.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client to create the message with.
    
    channel : ``Channel``
        Channel to send the message to.
    
    components : ``list<Component>``
        Components to send.
    
    Returns
    -------
    message_and_set_as_notified : ``(None | Message, bool)``
    """
    try:
        message = await client.message_create(
            channel,
            allowed_mentions = None,
            components = components,
        )
    except GeneratorExit:
        raise
    
    except ConnectionError:
        return None, False
    
    except DiscordException as exception:
        # server error, pretty normal at this point lol
        if exception.status >= 500:
            return None, False
        
        # Cant send message to user
        if exception.code in (
            ERROR_CODES.cannot_message_user_0, # user has dm-s disallowed
            ERROR_CODES.cannot_message_user_1, # user has dm-s disallowed
        ):
            return None, True
        
        raise
    
    return message, False
