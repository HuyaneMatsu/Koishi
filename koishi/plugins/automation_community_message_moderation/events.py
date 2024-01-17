__all__ = ()

from datetime import datetime as DateTime
from math import ceil

from hata import Permission, DiscordException, ERROR_CODES

from ...bot_utils.multi_client_utils import get_first_client_with_permissions
from ...bots import FEATURE_CLIENTS

from ..automation_core import get_community_message_moderation_fields
from ..blacklist_core import is_user_id_in_blacklist

from .cache import get_lock_for, delete_lock_of
from .helpers import sum_votes


PERMISSIONS_MASK_ACTION_REQUIRED = Permission().update_by_keys(manage_messages = True, view_channel = True)


@FEATURE_CLIENTS.events
async def reaction_add(client, event):
    """
    Handles a reaction add event.
    
    If the message's vote's match or exceed the limit the client deletes the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    event : ``ReactionAddEvent``
        The client who received the event.
    """
    await handle_reaction_event(client, event.message, event.emoji, event.user, True)
    

@FEATURE_CLIENTS.events
async def reaction_delete(client, event):
    """
    Handles a reaction remove event.
    
    If the message's vote's match or exceed the limit the client deletes the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    event : ``ReactionDeleteEvent``
        The client who received the event.
    """
    await handle_reaction_event(client, event.message, event.emoji, event.user, False)


@FEATURE_CLIENTS.events
async def reaction_delete_emoji(client, message, emoji, removed_reactions):
    """
    Handles a reaction emoji remove event.
    
    If the message's vote's match or exceed the limit the client deletes the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client: ``Client``
        The client who received the event.
    message: ``Message``
        The message from which the reactions were removed from.
    emoji : ``Emoji``
        The emoji of which the reactions were removed.
    removed_reactions : `None | dict<Reaction, ReactionMappingLine>`
        The removed reactions.
    """
    await handle_reaction_event(client, message, emoji, None, False)


async def handle_reaction_event(client, message, emoji, user, addition):
    """
    Handles a reaction add / remove event.
    
    If the message's vote's match or exceed the limit the client deletes the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    message: ``Message``
        The message from which the reactions were removed from.
    emoji : ``Emoji``
        The emoji of which the reactions were removed.
    user : `None | ClientUserBase`
        The user who's reaction was removed. Applicable only if a single emoji was removed.
    addition : `bool`
        Whether the reaction was added or removed.
    """
    if (user is not None):
        if user.bot:
            return
        
        if is_user_id_in_blacklist(user.id):
            return
        
    # Check whether we have config.
    configuration = get_community_message_moderation_fields(message.guild_id)
    if configuration is None:
        return
    
    down_vote_emoji_id, up_vote_emoji_id, availability_duration, vote_threshold = configuration
    if emoji.id != (down_vote_emoji_id if addition else up_vote_emoji_id):
        return
    
    # Check multi-client case
    if client is not get_first_client_with_permissions(
        message.channel, FEATURE_CLIENTS, PERMISSIONS_MASK_ACTION_REQUIRED
    ):
        return
    
    # Check availability duration
    if ceil((DateTime.utcnow() - message.created_at).total_seconds()) > availability_duration:
        return
    
    async with get_lock_for(message):
        # Did we already delete the message??
        if message.deleted:
            return
        
        # `message.reactions` can not be `None` since we just added one.
        reactions = message.reactions
        if reactions is None:
            try:
                await client.message_get(message, force_update = True)
            except ConnectionError:
                return
            
            except DiscordException as exception:
                if exception.code not in (
                    ERROR_CODES.unknown_channel, # channel deleted
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.missing_access, # client removed
                ):
                    raise
                
                delete_lock_of(message)
                return
        
        # Sum votes
        vote_count = await sum_votes(client, message, down_vote_emoji_id)
        vote_count -= await sum_votes(client, message, up_vote_emoji_id)
        
        # Return if under
        if vote_count < vote_threshold:
            return
        
        try:
            await client.message_delete(message)
        except ConnectionError:
            return
        
        except DiscordException as exception:
            if exception.code not in (
                ERROR_CODES.unknown_channel, # channel deleted
                ERROR_CODES.unknown_message, # message deleted
                ERROR_CODES.missing_access, # client removed
            ):
                raise
        
        delete_lock_of(message)
