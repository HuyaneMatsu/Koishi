__all__ = ()

from itertools import chain

from hata import Client

from .logic import (
    reset_auto_posters, reset_channel, should_auto_post_in_channel, try_remove_channel, try_update_channel
)

SLASH_CLIENT: Client


@SLASH_CLIENT.events
async def channel_create(client, channel):
    if should_auto_post_in_channel(channel):
        try_update_channel(channel)


@SLASH_CLIENT.events
async def channel_delete(client, channel):
    try_remove_channel(channel)


@SLASH_CLIENT.events
async def channel_edit(client, channel, old_parameters):
    reset_channel(channel)


@SLASH_CLIENT.events
async def guild_create(client, guild):
    for channel in chain(guild.chanels.values(), guild.threads.values()):
        if should_auto_post_in_channel(channel):
            try_update_channel(channel)


@SLASH_CLIENT.events
async def guild_delete(client, guild, guild_profile):
    for channel in chain(guild.chanels.values(), guild.threads.values()):
         try_remove_channel(channel)


@SLASH_CLIENT.events
async def ready(client):
    client.events.remove(ready)
    reset_auto_posters()
