__all__ = ()

from ...bot_utils.multi_client_utils import get_first_client_in_channel_from, get_first_client_in_guild_from
from ...bots import FEATURE_CLIENTS

from ..automation_core import get_touhou_feed_enabled

from .logic import (
    reset_touhou_feeders, reset_channel, should_touhou_feed_in_channel, try_remove_channel, try_remove_guild,
    try_update_channel, try_update_guild
)


@FEATURE_CLIENTS.events
async def channel_create(client, channel):
    """
    Handles a channel create event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    channel : ``Channel``
        The created channel.
    """
    if client is not get_first_client_in_channel_from(channel, FEATURE_CLIENTS):
        return
    
    if not get_touhou_feed_enabled(channel.guild_id):
        return
        
    if not should_touhou_feed_in_channel(client, channel):
        return
        
    try_update_channel(channel)


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
    if client is not get_first_client_in_channel_from(channel, FEATURE_CLIENTS):
        return
    
    try_remove_channel(channel)


@FEATURE_CLIENTS.events
async def channel_update(client, channel, old_attributes):
    """
    Handles a channel update event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    channel : ``Channel``
        The affected channel.
    
    old_attributes : `dict<str, object>`
        The affected old attributes of the channel.
    """
    if not (
        ('applied_tag_ids' in old_attributes) or
        ('available_tags' in old_attributes) or
        ('name' in old_attributes) or
        ('permission_overwrites' in old_attributes) or
        ('status' in old_attributes) or
        ('topic' in old_attributes)
    ):
        return
    
    if client is not get_first_client_in_channel_from(channel, FEATURE_CLIENTS):
        return
    
    if not get_touhou_feed_enabled(channel.guild_id):
        return
    
    reset_channel(client, channel)


@FEATURE_CLIENTS.events
async def guild_create(client, guild):
    """
    Handles a guild create event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    guild : ``Guild``
        The created guild.
    """
    if client is not get_first_client_in_guild_from(guild, FEATURE_CLIENTS):
        return
    
    if not get_touhou_feed_enabled(guild.id):
        return
        
    try_update_guild(client, guild)


@FEATURE_CLIENTS.events
async def guild_delete(client, guild, guild_profile):
    """
    Handles a guild delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    guild : ``Guild``
        The deleted guild.
    
    guild_profile : ``GuildProfile``
        The client's guild profile at the guild.
    """
    if client.guilds:
        return
    
    if not get_touhou_feed_enabled(guild.id):
        return
        
    try_remove_guild(guild)


@FEATURE_CLIENTS.events
async def role_delete(client, role):
    """
    Handles a role delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    role : ``Role``
        The deleted role.
    """
    guild = role.guild
    if client is not get_first_client_in_guild_from(guild, FEATURE_CLIENTS):
        return
    
    if not get_touhou_feed_enabled(guild.id):
        return
    
    try_update_guild(client, guild)


@FEATURE_CLIENTS.events
async def role_update(client, role, old_attributes):
    """
    Handles a role update event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    role : ``Role``
        The affected role.
    
    old_attributes : `dict<str, object>`
        The affected old attributes of the role.
    """
    if not (
        ('permissions' in old_attributes) or
        ('position' in old_attributes)
    ):
        return
    
    if not client.has_role(role):
        return
    
    guild = role.guild
    if client is not get_first_client_in_guild_from(guild, FEATURE_CLIENTS):
        return
    
    if not get_touhou_feed_enabled(guild.id):
        return
    
    try_update_guild(client, guild)


@FEATURE_CLIENTS.events
async def guild_user_update(client, guild, user, old_attributes):
    """
    Handles a guild user update event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    guild : ``Guild``
        The guild where the action occurred.
    
    user : ``ClientUserBase``
        The affected user.
    
    old_attributes : `dict<str, object>`
        The affected old attributes of the guild profile.
    """
    if client is not user:
        return
    
    if not (
        ('role_ids' in old_attributes)
    ):
        return
    
    if client is not get_first_client_in_guild_from(guild, FEATURE_CLIENTS):
        return
    
    if not get_touhou_feed_enabled(guild.id):
        return
    
    try_update_guild(client, guild)


@FEATURE_CLIENTS.events
async def ready(client):
    """
    Handles a ready event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    """
    client.events.remove(ready)
    reset_touhou_feeders(client)
