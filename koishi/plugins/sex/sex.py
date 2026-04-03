__all__ = ()

from random import random

from hata import DiscordException, ERROR_CODES, Embed, Permission
from hata.ext.slash import abort

from ...bot_utils.constants import ROLE__SUPPORT__NSFW_ACCESS
from ...bot_utils.multi_client_utils import has_client_message_create_permissions
from ...bots import FEATURE_CLIENTS

from .constants import SEX_IMAGES
from .spam_lock import check_lock_and_limit_level


EXTRA_PERMISSIONS = Permission().update_by_keys(embed_links = True)


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def sex(client, interaction_event):
    """
    You horny? Try your luck!
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    embed : ``Embed``
    """
    if interaction_event.application_permissions & EXTRA_PERMISSIONS != EXTRA_PERMISSIONS:
        abort('Cannot execute this command without `embed links` permission.')
    
    value = random()
    
    # If the user has nsfw role increase their chance by 25%
    if interaction_event.user.has_role(ROLE__SUPPORT__NSFW_ACCESS):
        value *= 0.80
    
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
    
    level = check_lock_and_limit_level(interaction_event, level)
    
    response_embed = Embed().add_image(SEX_IMAGES[level])
    
    try:
        await client.interaction_response_message_create(interaction_event, embed = response_embed)
    except ConnectionError:
        return
    
    except DiscordException as exception:
        if exception.status >= 500:
            return
        
        if exception.code != ERROR_CODES.unknown_interaction:
            raise
    
    else:
        return
    
    if not has_client_message_create_permissions(interaction_event.channel, client, EXTRA_PERMISSIONS):
        return
    
    try:
        await client.message_create(interaction_event.channel, embed = response_embed)
    except ConnectionError:
        return
    
    except DiscordException as exception:
        if exception.status >= 500:
            return
        
        if exception.code not in (
            ERROR_CODES.unknown_message, # message deleted
            ERROR_CODES.unknown_channel, # message's channel deleted
            ERROR_CODES.missing_access, # client removed
            ERROR_CODES.missing_permissions, # permissions changed meanwhile
        ):
            raise
