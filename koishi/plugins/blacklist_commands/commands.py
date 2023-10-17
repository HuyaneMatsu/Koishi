__all__ = ()

from hata import User
from hata.ext.slash import InteractionResponse, abort

from ...bot_utils.constants import GUILD__SUPPORT
from ...bots import SLASH_CLIENT

from ..blacklist_core import (
    add_user_id_to_blacklist, build_blacklist_user_add_embed, build_blacklist_user_entry_embed,
    build_blacklist_user_remove_embed, is_user_id_in_blacklist, remove_user_id_from_blacklist
)


BLACKLIST_COMMAND = SLASH_CLIENT.interactions(
    None,
    name = 'blacklist',
    description = 'Blacklists a user from interacting with the application.',
    guild = GUILD__SUPPORT,
)


@BLACKLIST_COMMAND.interactions
async def add(
    client,
    event,
    user: (User, 'Select a user to blacklist.'),
):
    """
    Blacklists a user from interacting with the application.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    event : ``InteractionEvent``
        The received interaction event.
    user : ``ClientUserBase``
        The user to blacklist.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if client.is_owner(event.user):
        abort('Owner only')
        return
    
    success = await add_user_id_to_blacklist(user.id)
    
    return InteractionResponse(    
        embed = build_blacklist_user_add_embed(user, success),
        show_for_invoking_user_only = True,
    )


@BLACKLIST_COMMAND.interactions
async def remove(
    client,
    event,
    user: (User, 'Select a user to remove from blacklist.'),
):
    """
    Removes a user from the blacklist.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    event : ``InteractionEvent``
        The received interaction event.
    user : ``ClientUserBase``
        The user to remove from blacklist.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if client.is_owner(event.user):
        abort('Owner only')
        return
    
    success = await remove_user_id_from_blacklist(user.id)
    
    return InteractionResponse(    
        embed = build_blacklist_user_remove_embed(user, success),
        show_for_invoking_user_only = True,
    )


@BLACKLIST_COMMAND.interactions
async def check(
    client,
    event,
    user: (User, 'Select a user to check.'),
):
    """
    Checks whether the user is blacklisted.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    event : ``InteractionEvent``
        The received interaction event.
    user : ``ClientUserBase``
        The user to blacklist.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if client.is_owner(event.user):
        abort('Owner only')
        return
    
    blacklisted = is_user_id_in_blacklist(user.id)
    
    return InteractionResponse(    
        embed = build_blacklist_user_entry_embed(user, blacklisted),
        show_for_invoking_user_only = True,
    )
