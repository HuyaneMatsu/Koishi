__all__ = ()

from random import random

from hata import DiscordException, ERROR_CODES, Embed, Permission
from hata.ext.slash import abort

from ...bots import FEATURE_CLIENTS

from .constants import SEX_IMAGES
from .spam_lock import check_lock_and_limit_level


INTERACTION_PERMISSIONS = Permission().update_by_keys(embed_links = True)
MESSAGE_CREATE_PERMISSIONS = Permission().update_by_keys(send_messages = True, embed_links = True)


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def sex(client, event):
    """
    You horny? Try your luck!
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    embed : ``Embed``
    """
    if event.application_permissions & INTERACTION_PERMISSIONS != INTERACTION_PERMISSIONS:
        abort('Cannot execute this command without `embed links` permission.')
    
    value = random()
    if value > 0.150: # no sex
        level = 0
    
    elif value > 0.100: # maybe sex
        level = 1
    
    elif value > 0.060: # probably sex
        level = 2
    
    elif value > 0.035: # yes sex
        level = 3
    
    elif value > 0.020: # yes sex fast
        level = 4
    
    elif value > 0.010: # totally sex
        level = 5
    
    elif value > 0.002: # sex 2.0
        level = 6
    
    else: # yes sex (koishi)
        level = 7
    
    level = check_lock_and_limit_level(event, level)
    
    response_embed = Embed().add_image(SEX_IMAGES[level])
    
    try:
        await client.interaction_response_message_create(event, embed = response_embed)
    except ConnectionError:
        return
    
    except DiscordException as exception:
        if exception.status == 500:
            return
        
        if exception.code != ERROR_CODES.unknown_interaction:
            raise
    
    else:
        return
    
    if event.application_permissions & MESSAGE_CREATE_PERMISSIONS != MESSAGE_CREATE_PERMISSIONS:
        return
    
    try:
        await client.message_create(event.channel, embed = response_embed)
    except ConnectionError:
        return
    
    except DiscordException as exception:
        if exception.status == 500:
            return
        
        if exception.code not in (
            ERROR_CODES.unknown_message, # message deleted
            ERROR_CODES.unknown_channel, # message's channel deleted
            ERROR_CODES.missing_access, # client removed
            ERROR_CODES.missing_permissions, # permissions changed meanwhile
        ):
            raise
