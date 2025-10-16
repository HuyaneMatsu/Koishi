__all__ = ()

from hata import StickerType, parse_custom_emojis

from ...bot_utils.multi_client_utils import get_first_client_with_permissions
from ...bots import FEATURE_CLIENTS

from .constants import PERMISSION_MASK, TRACKING_QUERY_LOCK
from .tracking_queries import (
    execute_channel_delete, execute_emoji_delete, execute_guild_delete, execute_message_create, execute_message_delete,
    execute_message_update, execute_reaction_add, execute_reaction_clear, execute_reaction_delete,
    execute_reaction_delete_emoji, execute_sticker_delete
)


@FEATURE_CLIENTS.events
async def message_create(client, message):
    """
    Handles a message create event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    message : ``Message``
        The received message.
    """
    user = message.author
    if user.bot:
        return
    
    if client is not get_first_client_with_permissions(message.channel, FEATURE_CLIENTS, PERMISSION_MASK):
        return
    
    content = message.content
    if content is None:
        custom_emojis = None
    
    else:
        custom_emojis = parse_custom_emojis(content)
        if not custom_emojis:
            custom_emojis = None
    
    stickers = message.stickers
    if (stickers is not None):
        stickers = {sticker for sticker in stickers if sticker.type is StickerType.guild}
        if not stickers:
            stickers = None
    
    if (custom_emojis is None) and (stickers is None):
        return
    
    async with TRACKING_QUERY_LOCK:
        await execute_message_create(message, custom_emojis, stickers)


@FEATURE_CLIENTS.events
async def message_delete(client, message):
    """
    Handles a message delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    message : ``Message``
        The deleted message.
    """
    # Do not do bot check, because the user may have reacted on the bot's message.
    if client is not get_first_client_with_permissions(message.channel, FEATURE_CLIENTS, PERMISSION_MASK):
        return
    
    async with TRACKING_QUERY_LOCK:
        await execute_message_delete(message)


@FEATURE_CLIENTS.events
async def message_update(client, message, old_attributes):
    """
    Handles a message update event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    message : ``Message``
        The updated message.
    
    old_attributes : `None | dict<str, object>`
        The old attributes of the message that are known to be changed.
    """
    if client is not get_first_client_with_permissions(message.channel, FEATURE_CLIENTS, PERMISSION_MASK):
        return
    
    if (old_attributes is None):
        old_content = None
        old_content_known = False
    else:
        try:
            old_content = old_attributes['content']
        except KeyError:
            return
        
        old_content_known = True
    
    if (old_content is None):
        old_custom_emojis = None
    else:
        old_custom_emojis = parse_custom_emojis(old_content)
        if not old_custom_emojis:
            old_custom_emojis = None
    
    new_content = message.content
    if new_content is None:
        new_custom_emojis = None
    
    else:
        new_custom_emojis = parse_custom_emojis(new_content)
        if not new_custom_emojis:
            new_custom_emojis = None
    
    if not old_content_known:
        delete_old_emojis = None
        delete_all_old_emoji = True
        add_new_emojis = new_custom_emojis
    
    else:
        if old_custom_emojis == new_custom_emojis:
            return
        
        if (old_custom_emojis is None) or (new_custom_emojis is None):
            intersection = None
        
        else:
            intersection = old_custom_emojis & new_custom_emojis
            if not intersection:
                intersection = None
            
            else:
                old_custom_emojis.difference_update(intersection)
                if not old_custom_emojis:
                    old_custom_emojis = None
                
                new_custom_emojis.difference_update(intersection)
                if not new_custom_emojis:
                    new_custom_emojis = None
        
        if (old_custom_emojis is not None) and (intersection is None):
            delete_old_emojis = None
            delete_all_old_emoji = True
        else:
            delete_old_emojis = old_custom_emojis
            delete_all_old_emoji = False
        
        add_new_emojis = new_custom_emojis
    
    async with TRACKING_QUERY_LOCK:
        await execute_message_update(message, delete_old_emojis, delete_all_old_emoji, add_new_emojis)


@FEATURE_CLIENTS.events
async def reaction_add(client, event):
    """
    Handles a reaction add event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    event : ``ReactionAddEvent``
        The received event.
    """
    user = event.user
    if user.bot:
        return
    
    emoji = event.emoji
    if not emoji.is_custom_emoji():
        return
    
    message = event.message
    if client is not get_first_client_with_permissions(message.channel, FEATURE_CLIENTS, PERMISSION_MASK):
        return
    
    async with TRACKING_QUERY_LOCK:
        await execute_reaction_add(message, emoji, user)


@FEATURE_CLIENTS.events
async def reaction_delete(client, event):
    """
    Handles a reaction delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    event : ``ReactionDeleteEvent``
        The received event.
    """
    user = event.user
    if user.bot:
        return
    
    emoji = event.emoji
    if not emoji.is_custom_emoji():
        return
    
    message = event.message
    if client is not get_first_client_with_permissions(message.channel, FEATURE_CLIENTS, PERMISSION_MASK):
        return
    
    async with TRACKING_QUERY_LOCK:
        await execute_reaction_delete(message, emoji, user)


def _reaction_mapping_line_are_users_all_bot(reaction_mapping_line):
    """
    Returns whether all users are bots in the given reaction mapping line.
    
    Parameters
    ----------
    reaction_mapping_line : ``ReactionMappingLine``
        The reaction mapping line to check.
    
    Returns
    -------
    all_bots : `bool`
    """
    users = reaction_mapping_line.users
    known_user_count = 0 if users is None else len(users)
    
    if known_user_count != reaction_mapping_line.count:
        return False
    
    if (users is not None):
        for user in users:
            if not user.bot:
                return False
    
    return True


@FEATURE_CLIENTS.events
async def reaction_delete_emoji(client, message, emoji, removed_reactions):
    """
    Handles a reaction delete emoji event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    message : ``Message``
        The message the reaction emoji was deleted from.
    
    emoji : ``Emoji``
        The emoji the reactions were removed for.
    
    removed_reactions : ``None | dict<Reaction, ReactionMappingLine>``
        The removed reactions if known.
    """
    if not emoji.is_custom_emoji():
        return
    
    if (removed_reactions is not None):
        for reaction_mapping_line in removed_reactions.values():
            if not _reaction_mapping_line_are_users_all_bot(reaction_mapping_line):
                break
        else:
            return
    
    if client is not get_first_client_with_permissions(message.channel, FEATURE_CLIENTS, PERMISSION_MASK):
        return
    
    async with TRACKING_QUERY_LOCK:
        await execute_reaction_delete_emoji(message, emoji)


@FEATURE_CLIENTS.events
async def reaction_clear(client, message, reactions):
    """
    Handles a reaction clear event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    message : ``Message``
        The message the reactions were cleared from.
    
    reactions : `None | ReactionMapping`
        The removed reactions if known.
    """
    if (reactions is not None):
        for reaction, reaction_mapping_line in reactions.iter_items():
            if (
                reaction.emoji.is_custom_emoji() and
                not _reaction_mapping_line_are_users_all_bot(reaction_mapping_line)
            ):
                break
        else:
            return
    
    message = message
    if client is not get_first_client_with_permissions(message.channel, FEATURE_CLIENTS, PERMISSION_MASK):
        return
    
    async with TRACKING_QUERY_LOCK:
        await execute_reaction_clear(message)


@FEATURE_CLIENTS.events
async def emoji_delete(client, emoji):
    """
    Handles an emoji delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    emoji : ``Emoji``
        The deleted emoji.
    """
    guild = emoji.guild
    if (guild is not None):
        clients = guild.clients
        if clients and (client is not clients[0]):
            return
    
    async with TRACKING_QUERY_LOCK:
        await execute_emoji_delete(emoji)


@FEATURE_CLIENTS.events
async def sticker_delete(client, sticker):
    """
    Handles a sticker delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    sticker : ``Sticker``
        The deleted sticker.
    """
    guild = sticker.guild
    if (guild is not None):
        clients = guild.clients
        if clients and (client is not clients[0]):
            return
    
    async with TRACKING_QUERY_LOCK:
        await execute_sticker_delete(sticker)


@FEATURE_CLIENTS.events
async def channel_delete(client, channel):
    """
    Handles a channel delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    channel : ``Channel``
        The deleted channel.
    """
    guild = channel.guild
    if (guild is not None):
        clients = guild.clients
        if clients and (client is not clients[0]):
            return
    
    async with TRACKING_QUERY_LOCK:
        await execute_channel_delete(channel)


@FEATURE_CLIENTS.events
async def guild_delete(client, guild, guild_profile):
    """
    Handles a channel delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    guild : ``Guild``
        The deleted guild.
    
    guild_profile : `None | GuildProfile`
        The client's guild profile at the guild.
    """
    if guild.clients:
        return
    
    # Do not lock this one.
    await execute_guild_delete(guild)
