from hata.ext.extension_loader import require
require(SOLARLINK_VOICE=True)

from re import compile as re_compile, escape as re_escape, I as re_ignore_case
from functools import partial as partial_func
from math import ceil, floor

from hata import Client, is_url, Embed, CHANNELS, BUILTIN_EMOJIS, Emoji

from hata.ext.slash import abort, InteractionResponse, Select, Option, wait_for_component_interaction
from hata.ext.solarlink import SolarPlayer

from bot_utils.constants import GUILD__SUPPORT

EMOJI_CURRENT_TRACK = BUILTIN_EMOJIS['satellite']
EMOJI_QUEUE_TIME = BUILTIN_EMOJIS['clock1']
EMOJI_QUEUE_LENGTH = Emoji.precreate(704392145330634812)
EMOJI_BEHAVIOR = BUILTIN_EMOJIS['control_knobs']
EMOJI_CHANNEL = BUILTIN_EMOJIS['mega']
EMOJI_VOLUME = BUILTIN_EMOJIS['level_slider']

class Player(SolarPlayer):
    __slots__ = ('text_channel_id', )
    def __new__(cls, node, guild_id, channel_id):
        self = SolarPlayer.__new__(cls, node, guild_id, channel_id)
        self.text_channel_id = 0
        return self
    
    def set_text_channel(self, event):
        self.text_channel_id = event.channel_id
    
    @property
    def text_channel(self):
        text_channel_id = self.text_channel_id
        if text_channel_id:
            return CHANNELS[text_channel_id]
    
    @property
    def queue_duration(self):
        duration = 0.0
        
        for configured_track in self.iter_all_track():
            duration += configured_track.track.duration
        
        return duration


def duration_to_string(duration):
    duration = int(duration)
    seconds = duration % 60
    minutes = duration // 60
    hours = minutes // 60
    
    and_index = bool(hours) + bool(minutes) + bool(seconds)
    
    if and_index == 0:
        string = '0 seconds'
    
    else:
        index = 0
        string_parts = []
        for value, unit in zip(
            (hours, minutes, seconds),
            ('hours', 'minutes', 'seconds'),
        ):
            if not value:
                continue
                
            index += 1
            if index > 1:
                if index == and_index:
                    string_parts.append(' and ')
                else:
                    string_parts.append(', ')
            
            string_parts.append(str(value))
            string_parts.append(' ')
            string_parts.append(unit)
        
        string = ''.join(string_parts)
    
    return string


def get_behaviour_string(player):
    if player.is_repeating_queue():
        if player.is_shuffling():
            string = 'Repeating over the queue.'
        else:
            string = 'Repeating and shuffling the queue.'
    elif player.set_repeat_current():
        if player.is_shuffling():
            string = 'Repeating over the current track and shuffling????'
        else:
            string = 'Repeating over the current track.'
    else:
        if player.is_shuffling():
            string = 'No repeat, but shuffle queue.'
        else:
            string = 'No repeat, no shuffle.'
    
    return string

def add_track_title_to(add_to, track):
    title = track.title
    if len(title) > 50:
        add_to.append(title[:47])
        add_to.append('...')
    else:
        add_to.append(title)

def add_track_duration_to(add_to, track):
    duration = int(track.duration)
    add_to.append('(')
    add_to.append(str(duration//60))
    add_to.append(':')
    add_to.append(str(duration%60))
    add_to.append(')')

def add_track_short_description_to(add_to, track):
    # Add title
    url = track.url
    
    add_to.append('**')
    if (url is not None):
        add_to.append('[')
    
    add_track_title_to(add_to, track)
    
    add_to.append('**')
    if (url is not None):
        add_to.append('](')
        add_to.append(url)
        add_to.append(')')
    
    add_to.append(' ')
    
    add_track_duration_to(add_to, track)



def create_track_short_description(track):
    add_to = []
    add_track_short_description_to(add_to, track)
    return ''.join(add_to)


def add_track_short_field_description_to(add_to, configured_track):
    add_track_short_description_to(add_to, configured_track.track)
    
    add_to.append('\n**Queued by:** ')
    
    # Add who queued it
    add_to.append(configured_track.requested.full_name)
    
    return configured_track


def create_track_short_field_description(configured_track):
    add_to = []
    add_track_short_field_description_to(add_to, configured_track)
    return ''.join(add_to)

def add_song_selection_header(embed, user):
    return embed.add_author(
        user.avatar_url,
        'Song selection',
    )


def add_current_track_field(embed, player):
    track = player.get_current()
    if (track is not None):
        if player.is_paused():
            title = 'paused'
        else:
            title = 'playing'
        
        embed.add_field(
            f'{EMOJI_CURRENT_TRACK} currently {title}',
            create_track_short_field_description(track),
        )
    
    return embed


def create_added_music_embed(player, user, description):
    embed = Embed(
        None,
        description,
    )
    
    add_current_track_field(embed, player)
    add_song_selection_header(embed, user)
    
    return embed


LAVA_VOICE_TRACK_SELECT_CUSTOM_ID = 'lava_voice.select'

def create_track_select(tracks, length):
    options = []

    index = 0
    while True:
        option_value = str(index)
        
        track = tracks[index]
        index += 1
        
        option_label_parts = []
        
        option_label_parts.append(str(index))
        option_label_parts.append('. ')
        add_track_title_to(option_label_parts, track)
        option_label_parts.append(' ')
        add_track_duration_to(option_label_parts, track)
        
        option_label = ''.join(option_label_parts)
        
        options.append(Option(option_value, option_label))
        
        if index == length:
            break
    
    return Select(
        options,
        LAVA_VOICE_TRACK_SELECT_CUSTOM_ID,
        placeholder = 'Select a track to play',
        max_values = length,
    )
    
        
    

SLASH_CLIENT: Client


VOICE_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'voice',
    description = 'Voice commands',
    guild = GUILD__SUPPORT,
)


@VOICE_COMMANDS.interactions
async def pause(client, event):
    """Pauses the currently playing track."""
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('There is no player at the guild.')
        return
    
    if player.is_paused():
        title = 'Playing paused. (was paused before)'
    else:
        await player.pause()
        title = 'Playing paused.'
    
    embed = Embed(
        title,
    )
    
    track = player.get_current()
    if (track is not None):
        embed.add_field(
            f'{EMOJI_CURRENT_TRACK} Currently paused',
            create_track_short_field_description(track),
        )
    
    return embed


@VOICE_COMMANDS.interactions
async def resume(client, event):
    """Resumes the currently playing track."""
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('There is no player at the guild.')
        return
    
    if player.is_paused():
        await player.resume()
        title = 'Playing resumed.'
    else:
        title = 'Playing resumed. (was not paused before)'
    
    embed = Embed(
        title,
    )
    
    track = player.get_current()
    if (track is not None):
        embed.add_field(
            f'{EMOJI_CURRENT_TRACK} Currently playing',
            create_track_short_field_description(track),
        )
    
    return embed


@VOICE_COMMANDS.interactions
async def leave(client, event):
    """Leaves from the voice channel."""
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('There is no player at the guild.')
        return
    
    yield
    await player.disconnect()
    
    title =  f'{client.name_at(event.guild)} out.'
    
    embed = Embed(
        title,
    )
    
    track = player.get_current()
    if (track is not None):
        embed.add_field(
            f'{EMOJI_CURRENT_TRACK} Played',
            create_track_short_field_description(track),
        )
    
    queue_length = player.queue_length
    if queue_length:
        embed.add_field(
            'Queue cleared.',
            f'{queue_length} tracks removed.',
        )
    
    yield embed
    return


def check_is_user_same(user, event):
    return (user is event.user)


@VOICE_COMMANDS.interactions
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
        )
        
        add_song_selection_header(embed, user)
        
        yield embed
        return
    
    playlist_name = result.playlist_name
    selected_track_index = result.selected_track_index
    tracks = result.tracks
    
    length = len(tracks)
    description_parts = []
    
    # We are in a playlist
    if (playlist_name is not None):
        # All track selected -> add all
        if (selected_track_index == -1) or (selected_track_index >= length):
            if player is None:
                player = await client.solarlink.join_voice(channel, cls=Player)
            
            for track in tracks:
                await player.append(track, requester=user)
            
            description_parts.append('Playlist ')
            
            if len(playlist_name) > 60:
                description_parts.append(playlist_name[:57])
                description_parts.append('...')
            else:
                description_parts.append(playlist_name)
            description_parts.append('\' ')
            
            description_parts.append(str(length))
            description_parts.append(' tracks are added to the queue.\n\n')
            
            if length:
                if length > 5:
                    length_truncated = -(5-length)
                    length = 5
                else:
                    length_truncated = 0
                
                index = 0
                
                while True:
                    track = tracks[index]
                    index += 1
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
            
            if player is None:
                player = await client.solarlink.join_voice(channel, cls=Player)
            
            track = tracks[selected_track_index]
            await player.append(track, requester=user)
            
            description_parts.append('The selected track from ')
            
            if len(playlist_name) > 60:
                description_parts.append(playlist_name[:57])
                description_parts.append('...')
            else:
                description_parts.append(playlist_name)
            description_parts.append(' ')
            
            description_parts.append(' is added to the queue.\n\n')
            
            add_track_short_description_to(description_parts, track)
        
        yield create_added_music_embed(player, user, ''.join(description_parts))
        return
    
    if is_name_an_url:
        if player is None:
            player = await client.solarlink.join_voice(channel, cls=Player)
        
        track = tracks[0]
        await player.append(track, requester=user)
        
        description_parts.append('Track added to queue.\n\n')
        add_track_short_description_to(description_parts, track)
        
        yield create_added_music_embed(player, user, ''.join(description_parts))
        return
    
    if length > 5:
        length = 5
    
    index = 0
    while True:
        track = tracks[index]
        index += 1
        
        description_parts.append('**')
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
    ).add_author(
        user.avatar_url,
        'Song selection. Please select the song to play.',
    ).add_footer(
        'This timeouts in 30s.',
    )
    
    select = create_track_select(tracks, length)
    
    message = yield InteractionResponse(embed=embed, components=select)
    
    try:
        component_interaction = await wait_for_component_interaction(
            message,
            timeout = 30.0,
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
        ).add_author(
            user.avatar_url,
            'Song selection. Nothing was chosen.',
        ).add_footer(
            'Timeout occurred.',
        )
    
    else:
        options = component_interaction.interaction.options
        
        selected_tracks = []
        for option in options:
            selected_tracks.append(tracks[option])
        
        if player is None:
            player = await client.solarlink.join_voice(channel)
        
        for track in tracks:
            await player.append(track, requester=user)
            
        description_parts = []
        
        length = len(track)
        
        if length == 1:
            description_parts.append('Track added to queue.\n\n')
            add_track_short_description_to(description_parts, track)
        else:
            description_parts.append(str(length))
            description_parts.append('track added to queue.\n\n')
            
            while True:
                track = tracks[index]
                index += 1
                description_parts.append('**')
                description_parts.append(str(index))
                description_parts.append('.** ')
                
                add_track_short_description_to(description_parts, track)
                
                if index == length:
                    break
                
                description_parts.append('\n')
                continue
            
            description = ''.join(description_parts)
            description_parts = None # clear reference
            
            embed = create_added_music_embed(player, user, description)
    
    yield InteractionResponse(
        embed = embed,
        components = None,
        message = message,
        event = component_interaction,
    )
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
        volume = player.get_volume()
        return f'{EMOJI_VOLUME.as_emoji} Volume: {volume*100.:.0f}%'
    
    if volume <= 0:
        volume = 0.0
    elif volume >= 200:
        volume = 2.0
    else:
        volume /= 100.0
    
    await player.set_volume(volume)
    return f'{EMOJI_VOLUME.as_emoji} Volume set to: {volume*100.:.0f}%.'


@VOICE_COMMANDS.interactions
async def stop(client, event):
    """Nyahh, if you really want I can stop playing audio."""
    player = client.solarlink.get_player(event.guild_id)

    if player is None:
        abort('There is no player at the guild.')
        return

    await player.stop()
    return 'Stopped playing'

BEHAVIOR_NAME_REPEAT_CURRENT = 'loop current'
BEHAVIOR_NAME_REPEAT_QUEUE = 'loop queue'
BEHAVIOR_NAME_SHUFFLE = 'shuffle'

BEHAVIOR_VALUE_GET = 0
BEHAVIOR_VALUE_REPEAT_CURRENT = 1
BEHAVIOR_VALUE_REPEAT_QUEUE = 2
BEHAVIOR_VALUE_SHUFFLE = 3

BEHAVIOR_CHOICES = [
    (BEHAVIOR_NAME_REPEAT_CURRENT, BEHAVIOR_VALUE_REPEAT_CURRENT),
    (BEHAVIOR_NAME_REPEAT_QUEUE, BEHAVIOR_VALUE_REPEAT_QUEUE),
    (BEHAVIOR_NAME_SHUFFLE, BEHAVIOR_VALUE_SHUFFLE),
]

@VOICE_COMMANDS.interactions
async def behaviour_(client, event,
    behaviour : (BEHAVIOR_CHOICES, 'Choose a behavior') = BEHAVIOR_VALUE_GET,
    value : (bool, 'Set value') = True,
):
    """Get or set the player's behaviour."""
    player = client.solarlink.get_player(event.guild_id)

    if player is None:
        abort('There is no player at the guild.')
        return
    
    if behaviour == BEHAVIOR_VALUE_GET:
        content = get_behaviour_string(player)
    
    elif behaviour == BEHAVIOR_VALUE_REPEAT_CURRENT:
        player.set_repeat_current(value)
        if value:
            content = 'Started to repeat the current track.'
        else:
            content = 'Stopped to repeat the current track.'
    
    elif behaviour == BEHAVIOR_VALUE_REPEAT_QUEUE:
        player.set_repeat_queue(value)
        if value:
            content = 'Started to repeat the whole queue.'
        else:
            content = 'Stopped to repeat the whole queue.'
        
    elif behaviour == BEHAVIOR_VALUE_SHUFFLE:
        player.set_shuffle(value)
        if value:
            content = 'Started shuffling the queue.'
        else:
            content = 'Stopped to shuffle the queue.'
    
    else:
        return # ?
    
    return content


def generate_track_autocomplete_form(configured_track):
    track = configured_track.track
    result = f'{track.title} by {track.author}'
    if len(result) > 69:
        result = result[:66] + '...'
    
    return result


@VOICE_COMMANDS.interactions
async def skip(client, event,
    track : ('str', 'Which track to skip?') = None,
):
    """Skips the selected track."""
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('There is no player at the guild.')
        return
    
    if track is None:
        index = 0
    else:
        for index, configured_track in enumerate(player.iter_all_track()):
            if generate_track_autocomplete_form(configured_track) == track:
                break
        else:
            index = -1
    
    configured_track = await player.spip(index)
    if configured_track is None:
        return 'Nothing was skipped.'
    
    description_parts = ['Track skipped: ']
    add_track_short_description_to(description_parts, configured_track.track)
    description = ''.join(description_parts)
    
    return create_added_music_embed(player, event.user, description)


@VOICE_COMMANDS.interactions
async def remove(client, event,
    track : ('str', 'Which track to skip?') = None,
):
    """Removes the selected track from the queue"""
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('There is no player at the guild.')
        return
    
    if track is None:
        index = 0
    else:
        for index, configured_track in enumerate(player.iter_all_track()):
            if generate_track_autocomplete_form(configured_track) == track:
                break
        else:
            index = -1
    
    configured_track = await player.remove(index)
    if configured_track is None:
        return 'Nothing was removed.'
    
    description_parts = ['Track removed: ']
    add_track_short_description_to(description_parts, configured_track.track)
    description = ''.join(description_parts)
    
    return create_added_music_embed(player, event.user, description)


@skip.autocomplete('track')
@remove.autocomplete('track')
async def autocomplete_skip_track(client, event, value):
    player = client.solarlink.get_player(event.guild_id)
    if player is None:
        return None
    
    collected = 0
    track_names = []
    
    if value is None:
        for configured_track in player.iter_all_track():
            track_names.append(generate_track_autocomplete_form(configured_track))
            
            collected += 1
            if collected == 20:
                break
    else:
        pattern = re_compile(re_escape(value), re_ignore_case)
        
        for configured_track in player.iter_all_track():
            track_name = generate_track_autocomplete_form(configured_track)
            if (pattern.search(track_name) is not None):
                track_names.append(track_name)
            
            collected += 1
            if collected == 20:
                break
    
    return track_names


@VOICE_COMMANDS.interactions
async def queue_(client, event,
    page: (int, 'Which page to show?') = 0,
):
    """Shows the track queue for the current guild."""
    player = client.solarlink.get_player(event.guild_id)
    if player is None:
        embed = Embed(
            None,
            '**Once there were heart throbbing adventures, but now, one can find only dust and decay.**'
        )
    else:

        queue = player.queue
        length = len(queue)
        limit_low = page*5
        limit_high = limit_low+5
        if limit_high > length:
            limit_high = length
        
        if limit_low < limit_high:
            index = limit_low
            description_parts = []
            
            while True:
                track = queue[index]
                index += 1
                description_parts.append('**')
                description_parts.append(str(index))
                description_parts.append('.** ')
                
                add_track_short_description_to(description_parts, track)
                
                if index == limit_high:
                    break
                
                description_parts.append('\n')
                continue
            
            description = ''.join(description_parts)
        else:
            description = None
        
        embed = Embed(None, description)
        
        page_count = ceil(length/5.0)
        embed.add_footer(f'Page {page} / {page_count}')
        
        add_current_track_field(embed, player)
        
        embed.add_field(
            f'{EMOJI_QUEUE_LENGTH} queue length',
            str(length),
            inline = True,
        )
        
        embed.add_field(
            f'{EMOJI_QUEUE_TIME} queue duration',
            duration_to_string(player.queue_duration),
            inline = True,
        )
        
        voice_channel = player.channel
        if voice_channel is None:
            # not in cache
            voice_channel_name = '#unknown'
        else:
            voice_channel_name = voice_channel.name
        
        embed.add_field(
            f'{EMOJI_CHANNEL} playing in',
            voice_channel_name,
        )
        
        embed.add_field(
            f'{EMOJI_CHANNEL} playing in',
            voice_channel_name,
        )
    
        embed.add_field(
            f'{EMOJI_BEHAVIOR} behavior',
            get_behaviour_string(player),
            inline = True
        )
        
        embed.add_field(
            f'{EMOJI_VOLUME} volume',
            f'{player.get_volume()*100.:.0f}%',
            inline = True,
        )
    
    
    guild = event.guild
    if guild is None:
        author_icon_url = None
        author_name = 'Queue'
    else:
        author_icon_url = guild.icon_url_as(size=64)
        author_name = f'Queue for {guild.name}'
    
    embed.add_author(author_icon_url, author_name)
    return embed
