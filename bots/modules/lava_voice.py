from hata import Client, is_url, Embed
from hata.ext.extension_loader import require
from hata.ext.commands import abort

from bot_utils.constants import GUILD__SUPPORT

require(LAVALINK_VOICE=True)

SLASH_CLIENT: Client

VOICE_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'voice',
    description = 'Voice commands',
    guild = GUILD__SUPPORT,
)

@VOICE_COMMANDS.interactions
async def join(client,
    volume : ('int', 'Any preset volume?') = None,
):
    """Joins the voice channel."""
    state = guild.voice_states.get(user.id, None)
    if state is None:
        abort('You must be in a voice channel to invoke this command.')
        return
    
    channel = state.channel
    if not channel.cached_permissions_for(client).can_connect:
        abort(f'I have no permissions to connect to {channel.mention}.')
        return
    
    yield
    
    player = await client.solarlink.join_voice(channel)
    
    content = f'Joined to {state.channel.name}'
    
    if (volume is not None):
        if volume <= 0:
            volume = 0.0
        elif volume >= 200:
            volume = 2.0
        else:
            volume /= 100.0
        
        await player.set_volume(volume)
        content = f'{content}; Volume set to {volume*100.:.0f}%'
    
    yield content
    return


@VOICE_COMMANDS.interactions
async def pause(client, event):
    """Pauses the currently playing track."""
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('There is no player at the guild.')
        return
    
    await player.pause()
    return 'Player paused.'


@VOICE_COMMANDS.interactions
async def resume(client, event):
    """Resumes the currently playing track."""
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('There is no player at the guild.')
        return
    
    await player.resume()
    return 'Playing resumed.'


@VOICE_COMMANDS.interactions
async def leave(client, event):
    """Leaves from the voice channel."""
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('There is no player at the guild.')
        return
    
    yield
    await player.disconnect()
    yield f'{client.name_at(event_or_message.guild)} out.'
    return


@VOICE_COMMANDS.interactions
async def play(client, event,
    name: ('str', 'The name of the audio to play.')
):
    """Plays an audio from youtube."""
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('There is no player at the guild.')
        return
    
    yield
    
    if not is_url(name):
        name = f'ytsearch:{name}'
    
    result = await client.solarlink.get_tracks(name)
    
    # Case 0, there are 0 tracks
    if result is None:
        yield Embed('Nothing found.')
        return
    
    playlist_name = result.playlist_name
    if playlist_name is None:
        index = result.selected_track_index
        if index == -1:
            index = 0
    else:
        index = result.selected_track_index
        if index == -1:
            if len(result.tracks):
                abort(f'Playlist {playlist_name} has no selected track.')
            else:
                abort(f'Playlist {playlist_name} is empty.')
            return
    
    tracks = result.tracks
    if index >= len(tracks):
        index = 0
    
    track = tracks[index]
    
    requested_at = event.created_at
    
    started_playing = await player.append(track, requested_at=requested_at, requester=user)
    
    if started_playing:
        title = 'Started to play track'
    else:
        title = 'Track put on queue.'
    
    embed = Embed(
        title,
        (
            f'By: {track.author}\n'
            f'Duration: {trackduration:.0f}s'
        ),
        timestamp = event.requested_at,
    ).add_footer(
        f'Track requested by {user.full_name}',
        icon_url = user.avatar_url,
    )
    
    yield InteractionResponse(embed=embed, allowed_mentions=None)
    return


@VOICE_COMMANDS.interactions
async def volume_(client, event,
    volume: ('number', 'Percentage?') = None,
):
    """Gets or sets my volume to the given percentage."""
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('There is no player at the guild.')
        return
    
    if volume is None:
        return f'{voice_client.volume*100.:.0f}%'
    
    if volume <= 0:
        volume = 0.0
    elif volume >= 200:
        volume = 2.0
    else:
        volume /= 100.0
    
    await do_set_volume(voice_client, volume)
    return f'Volume set to {volume*100.:.0f}%.'
