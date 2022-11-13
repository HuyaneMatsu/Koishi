__all__ = ()

from scarletio import to_coroutine
from hata import Client, Embed
from hata.ext.solarlink import TRACK_END_REASONS

from .constants import EMBED_COLOR, EMOJI_LAST_TRACK, EMOJI_CURRENT_TRACK, LEAVE_TIMEOUT
from .helpers import create_track_short_field_description


SLASH_CLIENT: Client


def can_send_message_in_channel(client, channel):
    if (channel is not None):
        permissions = channel.cached_permissions_for(client)
        if channel.is_in_group_thread():
            if permissions.can_send_messages_in_threads:
                return True
        
        else:
            if permissions.can_send_messages:
                return True
    
    return False


async def notify_leave(client, player):
    channel = player.channel
    if not can_send_message_in_channel(client, channel):
        return
    
    embed = Embed(
        f'There are no users listening in {channel.name}.',
        color = EMBED_COLOR,
    ).add_footer(
        f'I will leave from the channel after {LEAVE_TIMEOUT:.0f} seconds.',
    )
    
    await client.message_create(channel, embed = embed)


@SLASH_CLIENT.events
async def track_end(client, event):
    if event.reason != TRACK_END_REASONS.finished:
        return
    
    player = event.player
    new_track = player.get_current()
    old_track = event.track
    if new_track is old_track:
        return
    
    channel = player.channel
    if not can_send_message_in_channel(client, channel):
        return
    
    embed = Embed(color = EMBED_COLOR)
    
    embed.add_field(
        f'{EMOJI_LAST_TRACK} Finished playing',
        create_track_short_field_description(old_track),
    )
    
    if (new_track is not None):
        embed.add_field(
            f'{EMOJI_CURRENT_TRACK} Started playing',
            create_track_short_field_description(new_track),
        )
    
    await client.message_create(
        channel,
        embed = embed,
    )


@SLASH_CLIENT.events
async def track_exception(client, event):
    old_track = event.track
    new_track = event.player.get_current()

    
    channel = event.player.channel
    if not can_send_message_in_channel(client, channel):
        return
    
    embed = Embed(color = EMBED_COLOR)
    
    embed.add_field(
        f'{EMOJI_LAST_TRACK} Something went wrong meanwhile playing',
        create_track_short_field_description(old_track),
    )
    
    if (new_track is not None):
        embed.add_field(
            f'{EMOJI_CURRENT_TRACK} Started playing',
            create_track_short_field_description(new_track),
        )
    
    await client.message_create(
        channel,
        embed = embed,
    )


@SLASH_CLIENT.events
async def user_voice_join(client, voice_state):
    player = client.solarlink.get_player(voice_state.guild_id)
    if (player is not None):
        player.check_auto_leave()


@SLASH_CLIENT.events
async def user_voice_leave(client, voice_state, old_channel_id):
    player = client.solarlink.get_player(voice_state.guild_id)
    if (player is not None) and player.check_auto_leave():
           await notify_leave(client, player)


@SLASH_CLIENT.events
async def user_voice_update(client, voice_state, old_attributes):
    player = client.solarlink.get_player(voice_state.guild_id)
    if (player is not None) and player.check_auto_leave():
           await notify_leave(client, player)


@SLASH_CLIENT.events
async def user_voice_update(client, voice_state, old_channel_id):
    player = client.solarlink.get_player(voice_state.guild_id)
    if (player is not None):
        if player.check_auto_leave():
           await notify_leave(client, player)


@SLASH_CLIENT.events
@to_coroutine
def voice_client_move(client, voice_state, old_channel_id):
    yield
    
    player = client.solarlink.get_player(voice_state.guild_id)
    if (player is not None):
        if player.check_auto_leave():
           yield from notify_leave(client, player).__await__()
