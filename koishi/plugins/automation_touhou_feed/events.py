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
    if client is not get_first_client_in_channel_from(channel, FEATURE_CLIENTS):
        return
    
    if not get_touhou_feed_enabled(channel.guild_id):
        return
        
    if not should_touhou_feed_in_channel(client, channel):
        return
        
    try_update_channel(channel)


@FEATURE_CLIENTS.events
async def channel_delete(client, channel):
    if client is not get_first_client_in_channel_from(channel, FEATURE_CLIENTS):
        return
    
    try_remove_channel(channel)


@FEATURE_CLIENTS.events
async def channel_edit(client, channel, old_parameters):
    if client is not get_first_client_in_channel_from(channel, FEATURE_CLIENTS):
        return
    
    if not get_touhou_feed_enabled(channel.guild_id):
        return
    
    reset_channel(client, channel)


@FEATURE_CLIENTS.events
async def guild_create(client, guild):
    if client is not get_first_client_in_guild_from(guild, FEATURE_CLIENTS):
        return
    
    if not get_touhou_feed_enabled(guild.id):
        return
        
    try_update_guild(client, guild)


@FEATURE_CLIENTS.events
async def guild_delete(client, guild, guild_profile):
    if client.guilds:
        return
    
    if not get_touhou_feed_enabled(guild.id):
        return
        
    try_remove_guild(guild)


@FEATURE_CLIENTS.events
async def ready(client):
    client.events.remove(ready)
    reset_touhou_feeders(client)
