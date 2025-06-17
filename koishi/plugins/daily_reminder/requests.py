__all__ = ()

from hata import DiscordException, ERROR_CODES

from ...bot_utils.user_getter import get_user

from .queries import set_entry_as_notified_with_connector


async def try_user_get(user_id, entry_id, connector):
    """
    Tries to get the user. On success returns it.
    If it cannot get the user sets that they were already notified to avoid repeat.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier to get.
    entry_id : `int`
        The entry's id to interact with as required.
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    user : `None | ClientUserBase`
    """
    try:
        user = await get_user(user_id)
    except GeneratorExit:
        raise
    
    except ConnectionError:
        return
    
    except DiscordException as exception:
        # server error, pretty normal at this point lol
        if exception.status >= 500:
            return
        
        # user deleted
        if exception.code == ERROR_CODES.unknown_user:
            await set_entry_as_notified_with_connector(connector, entry_id)
            return
        
        raise
    
    return user


async def try_channel_create(client, user_id, entry_id, connector):
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
    entry_id : `int`
        The entry's id to interact with as required.
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    channel : `None | Channel`
    """
    try:
        channel = await client.channel_private_create(user_id)
    except GeneratorExit:
        raise
    
    except ConnectionError:
        return
    
    except DiscordException as exception:
        # server error, pretty normal at this point lol
        if exception.status >= 500:
            return
        
        # user deleted
        if exception.code == ERROR_CODES.unknown_user:
            await set_entry_as_notified_with_connector(connector, entry_id)
            return
        
        raise
    
    return channel


async def try_message_create(client, channel, embed, components, entry_id, connector):
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
    embed : ``Embed``
        Embed to send.
    components : ``Component``
        Component(s) to send.
    entry_id : `int`
        The entry's id to interact with as required.
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    message : ``None | Message``
    """
    try:
        message = await client.message_create(
            channel,
            allowed_mentions = None,
            embed = embed,
            components = components,
        )
    except GeneratorExit:
        raise
    
    except ConnectionError:
        return
    
    except DiscordException as exception:
        # server error, pretty normal at this point lol
        if exception.status >= 500:
            return
        
        # Cant send message to user
        if exception.code == ERROR_CODES.cannot_message_user:
            await set_entry_as_notified_with_connector(connector, entry_id)
            return
        
        raise
    
    return message
