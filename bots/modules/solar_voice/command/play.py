from hata import Embed, is_url
from hata.ext.slash import SlasherApplicationCommand, abort, InteractionResponse, wait_for_component_interaction
from hata.ext.extension_loader import import_extension
from random import choice
from functools import partial as partial_func


EMBED_COLOR, TRACK_EMOJIS, TRACK_PER_PAGE, LEAVE_TIMEOUT = import_extension(
    '..constants', 'EMBED_COLOR', 'TRACK_EMOJIS', 'TRACK_PER_PAGE', 'LEAVE_TIMEOUT'
)
(
    add_current_track_field,
    add_song_selection_header,
    add_track_short_description_to,
    create_added_music_embed,
    create_track_select,
) = import_extension('..helpers',
    'add_current_track_field',
    'add_song_selection_header',
    'add_track_short_description_to',
    'create_added_music_embed',
    'create_track_select',
)
Player = import_extension('..player', 'Player')

COMMAND: SlasherApplicationCommand


def check_is_user_same(user, event):
    return (user is event.user)


@COMMAND.interactions
async def play(client, event,
    name: ('str', 'The name of the audio to play.')
):
    """Plays an audio from youtube."""
    player = client.solarlink.get_player(event.guild_id)
    
    user = event.user
    
    if player is None:
        guild = event.guild
        if guild is None:
            abort('Please use this command inside of a guild.')
        
        state = guild.voice_states.get(user.id, None)
        if state is None:
            abort(f'Please join a voice channel first, so I will know where to play.')
        
        channel = state.channel
        if not channel.cached_permissions_for(client).can_connect:
            abort(f'I have no permissions to connect to your channel: {channel.mention}.')
    
    yield
    
    if is_url(name):
        is_name_an_url = True
    else:
        is_name_an_url = False
        name = f'ytsearch:{name}'
    
    result = await client.solarlink.get_tracks(name)
    
    
    # Case 0, there are 0 tracks
    if result is None:
        embed = Embed(
            None,
            '*no result*',
            color = EMBED_COLOR,
        )
        
        add_song_selection_header(embed, 'Track selection', user)
        
        yield embed
        return
    
    playlist_name = result.playlist_name
    selected_track_index = result.selected_track_index
    tracks = result.tracks
    
    length = len(tracks)
    description_parts = []
    
    if player is None:
        join_player = True
    else:
        join_player = False
    
    # We are in a playlist
    if (playlist_name is not None):
        # All track selected -> add all
        title_parts = []
        
        if (selected_track_index <= 0) or (selected_track_index >= length):
            if join_player:
                player = await client.solarlink.join_voice(channel, cls=Player)
            
            player.set_text_channel(event)
            
            emojis = [choice(TRACK_EMOJIS) for index in range(length)]
            
            for (track, emoji) in zip(tracks, emojis):
                await player.append(track, requester=user, emoji=emoji)
            
            title_parts.append(str(length))
            title_parts.append(' track from playlist ')
            
            if len(playlist_name) > 60:
                title_parts.append(playlist_name[:57])
                title_parts.append('...')
            else:
                title_parts.append(playlist_name)
            title_parts.append(' added to the queue')
            
            if length:
                if length > TRACK_PER_PAGE:
                    length_truncated = -(TRACK_PER_PAGE - length)
                    length = TRACK_PER_PAGE
                else:
                    length_truncated = 0
                
                index = 0
                
                while True:
                    track = tracks[index]
                    emoji = emojis[index]
                    index += 1
                    description_parts.append(emoji.as_emoji)
                    description_parts.append(' ')
                    description_parts.append('**')
                    description_parts.append(str(index))
                    description_parts.append('.** ')
                    
                    add_track_short_description_to(description_parts, track)
                    
                    if index == length:
                        break
                    
                    description_parts.append('\n')
                    continue
                
                if length_truncated:
                    description_parts.append('\n\n')
                    description_parts.append(str(length_truncated))
                    description_parts.append(' more hidden.')
        
        else:
            # 1 Track is selected, add only that one
            
            if join_player:
                player = await client.solarlink.join_voice(channel, cls=Player)
            
            player.set_text_channel(event)
            
            emoji = choice(TRACK_EMOJIS)
            track = tracks[selected_track_index]
            await player.append(track, requester=user, emoji=emoji)
            
            title_parts.append('Track from ')
            
            if len(playlist_name) > 60:
                title_parts.append(playlist_name[:57])
                title_parts.append('...')
            else:
                title_parts.append(playlist_name)
            title_parts.append(' ')
            
            title_parts.append(' added to the queue.')
            
            description_parts.append(emoji.as_emoji)
            description_parts.append(' ')
            add_track_short_description_to(description_parts, track)
        
        yield create_added_music_embed(player, user, ''.join(title_parts), ''.join(description_parts))
        return
    
    if is_name_an_url:
        if join_player:
            player = await client.solarlink.join_voice(channel, cls=Player)
        
        player.set_text_channel(event)
        
        track = tracks[0]
        emoji = choice(TRACK_EMOJIS)
        await player.append(track, requester=user, emoji=emoji)
        
        description_parts.append(emoji.as_emoji)
        description_parts.append(' ')
        add_track_short_description_to(description_parts, track)
        
        yield create_added_music_embed(player, user, 'Track added to queue', ''.join(description_parts))
        return
    
    if length > TRACK_PER_PAGE:
        length = TRACK_PER_PAGE
    
    emojis = [choice(TRACK_EMOJIS) for index in range(length)]
    
    index = 0
    while True:
        track = tracks[index]
        emoji = emojis[index]
        index += 1
        
        description_parts.append(emoji.as_emoji)
        description_parts.append(' ')
        description_parts.append(' **')
        description_parts.append(str(index))
        description_parts.append('.** ')
        add_track_short_description_to(description_parts, track)
        
        if index == length:
            break
        
        description_parts.append('\n')
        continue
    
    description = ''.join(description_parts)
    description_parts = None # clear up reference
    
    embed = Embed(
        None,
        description,
        color = EMBED_COLOR,
    ).add_author(
        'Song selection | Please select the song(s) to play',
        user.avatar_url,
    ).add_footer(
        'This timeouts in 60 seconds.',
    )
    
    select = create_track_select(tracks, length)
    
    message = yield InteractionResponse(embed=embed, components=select)
    
    try:
        component_interaction = await wait_for_component_interaction(
            message,
            timeout = 60.0,
            check = partial_func(check_is_user_same, user)
        )
    
    except TimeoutError:
        component_interaction = None
        cancelled = True
    else:
        cancelled = False
    
    if cancelled:
        embed = Embed(
            None,
            description,
            color = EMBED_COLOR,
        ).add_author(
            'Song selection | Nothing was chosen',
            user.avatar_url,
        ).add_footer(
            'Timeout occurred.',
        )
    
    else:
        options = component_interaction.interaction.options
        
        selected_tracks_and_emojis = []
        for option in options:
            try:
                option = int(option)
            except ValueError:
                pass
            else:
                selected_tracks_and_emojis.append((
                    tracks[option],
                    emojis[option],
                ))
        
        if join_player:
            player = await client.solarlink.join_voice(channel, cls=Player)
        
        player.set_text_channel(event)
        
        for track, emoji in selected_tracks_and_emojis:
            await player.append(track, requester=user, emoji=emoji)
        
        description_parts = []
        
        length = len(selected_tracks_and_emojis)
        
        if length == 1:
            title = 'Track added to queue.'
            add_track_short_description_to(description_parts, track)
        else:
            title = f'{length} track added to queue'
            
            index = 0
            
            while True:
                track, emoji = selected_tracks_and_emojis[index]
                index += 1
                
                description_parts.append('**')
                description_parts.append(str(index))
                description_parts.append('.** ')
                description_parts.append(emoji.as_emoji)
                description_parts.append(' ')
                
                add_track_short_description_to(description_parts, track)
                
                if index == length:
                    break
                
                description_parts.append('\n')
                continue
        
        description = ''.join(description_parts)
        description_parts = None # clear reference
        
        embed = create_added_music_embed(player, user, title, description)
    
    
    if join_player and player.check_auto_leave():
        embed.add_footer(
            f'There are no users listening in {channel.name}. '
            f'I will leave from the channel after {LEAVE_TIMEOUT:.0f} seconds.'
        )
    
    
    yield InteractionResponse(
        embed = embed,
        components = None,
        message = message,
        event = component_interaction,
    )
    return
