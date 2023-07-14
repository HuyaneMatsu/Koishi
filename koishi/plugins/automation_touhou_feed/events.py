__all__ = ()

from ...bots import SLASH_CLIENT

from ..automation_core import get_touhou_feed_enabled

from .logic import (
    reset_auto_posters, reset_channel, should_auto_post_in_channel, try_remove_channel, try_remove_guild,
    try_update_channel, try_update_guild
)


@SLASH_CLIENT.events
async def channel_create(client, channel):
    if get_touhou_feed_enabled(channel.guild_id):
        if should_auto_post_in_channel(client, channel):
            try_update_channel(channel)


@SLASH_CLIENT.events
async def channel_delete(client, channel):
    try_remove_channel(channel)


@SLASH_CLIENT.events
async def channel_edit(client, channel, old_parameters):
    if get_touhou_feed_enabled(channel.guild_id):
        reset_channel(client, channel)


@SLASH_CLIENT.events
async def guild_create(client, guild):
    if get_touhou_feed_enabled(guild.id):
        try_update_guild(client, guild)


@SLASH_CLIENT.events
async def guild_delete(client, guild, guild_profile):
    if get_touhou_feed_enabled(guild.id):
        try_remove_guild(guild)


@SLASH_CLIENT.events
async def ready(client):
    client.events.remove(ready)
    reset_auto_posters(client)
