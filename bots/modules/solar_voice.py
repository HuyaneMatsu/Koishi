from hata.ext.extension_loader import require
require(SOLARLINK_VOICE=True)

from re import compile as re_compile, escape as re_escape, I as re_ignore_case
from functools import partial as partial_func
from math import ceil, floor
from random import choice

from hata import Client, is_url, Embed, CHANNELS, BUILTIN_EMOJIS, Emoji, escape_markdown, Permission

from hata.ext.slash import abort, InteractionResponse, Select, Option, wait_for_component_interaction
from hata.ext.solarlink import SolarPlayer, TRACK_END_REASONS

from bot_utils.constants import GUILD__SUPPORT

EMOJI_CURRENT_TRACK = BUILTIN_EMOJIS['satellite']
EMOJI_LAST_TRACK = BUILTIN_EMOJIS['closed_umbrella']
EMOJI_QUEUE_TIME = BUILTIN_EMOJIS['clock1']
EMOJI_QUEUE_LENGTH = BUILTIN_EMOJIS['dango']
EMOJI_BEHAVIOR = BUILTIN_EMOJIS['control_knobs']
EMOJI_CHANNEL = BUILTIN_EMOJIS['mega']
EMOJI_VOLUME = BUILTIN_EMOJIS['level_slider']

TRACK_PER_PAGE = 10

TRACK_EMOJIS = [
    Emoji.precreate(704393708467912875),
    Emoji.precreate(748504187620294656),
    Emoji.precreate(748506469694963713),
    Emoji.precreate(748507069690282054),
    Emoji.precreate(812069466069663765),
    Emoji.precreate(825074491817852979),
    Emoji.precreate(846320146342477834),
    Emoji.precreate(852856910116945930),
    Emoji.precreate(852857235067371521),
    Emoji.precreate(853152183222272011),
    Emoji.precreate(853152183629774848),
    Emoji.precreate(853507411150897162),
    Emoji.precreate(853507411293765642),
    Emoji.precreate(853507411548831764),
    Emoji.precreate(853507411674661014),
    Emoji.precreate(853507411687112734),
    Emoji.precreate(853507412064600084),
    Emoji.precreate(853507412577484811),
    Emoji.precreate(853685522303680512),
    Emoji.precreate(855417900764626994),
    Emoji.precreate(858609857568964618),
]

class Player(SolarPlayer):
    __slots__ = ('text_channel_id', )
    def __new__(cls, node, guild_id, channel_id):
        self, waiter = SolarPlayer.__new__(cls, node, guild_id, channel_id)
        self.text_channel_id = 0
        return self, waiter
    
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
        
        for configured_track in self.queue:
            duration += configured_track.track.duration
        
        return duration


def duration_to_string(duration):
    duration = int(duration)
    seconds = duration % 60
    minutes = duration // 60
    hours = minutes // 60
    minutes %= 60
    
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


def get_behavior_string(player):
    if player.is_repeating_queue():
        if player.is_shuffling():
            string = 'Repeating over the queue.'
        else:
            string = 'Repeating and shuffling the queue.'
    elif player.is_repeating_current():
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
        title = title[:47]
        title = escape_markdown(title)
        add_to.append(title)
        add_to.append('...')
    else:
        title = escape_markdown(title)
        add_to.append(title)

def add_track_duration_to(add_to, track):
    duration = int(track.duration)
    add_to.append('(')
    add_to.append(str(duration//60))
    add_to.append(':')
    add_to.append(format(duration%60, '0>2'))
    add_to.append(')')

def add_track_short_description_to(add_to, track):
    # Add title
    url = track.url
    
    if (url is not None):
        add_to.append('[')
    
    add_to.append('**')
    add_track_title_to(add_to, track)
    add_to.append('**')
    
    if (url is not None):
        add_to.append('](')
        add_to.append(url)
        add_to.append(')')
    
    add_to.append(' ')
    
    add_track_duration_to(add_to, track)



def create_track_short_description(configured_track):
    add_to = []
    add_to.append(configured_track.emoji.as_emoji)
    add_to.append(' ')
    add_track_short_description_to(add_to, configured_track.track)
    return ''.join(add_to)


def add_track_short_field_description_to(add_to, configured_track):
    add_to.append(configured_track.emoji.as_emoji)
    add_to.append(' ')
    
    add_track_short_description_to(add_to, configured_track.track)
    
    add_to.append('\n**Queued by:** ')
    
    # Add who queued it
    add_to.append(configured_track.requester.full_name)
    
    return configured_track


def create_track_short_field_description(configured_track):
    add_to = []
    add_track_short_field_description_to(add_to, configured_track)
    return ''.join(add_to)

def add_song_selection_header(embed, title, user):
    return embed.add_author(
        user.avatar_url,
        title,
    )


def add_current_track_field(embed, player):
    track = player.get_current()
    if (track is not None):
        if player.is_paused():
            title = 'paused'
        else:
            title = 'playing'
        
        embed.add_field(
            f'{EMOJI_CURRENT_TRACK} Currently {title}',
            create_track_short_field_description(track),
        )
    
    return embed


def create_added_music_embed(player, user, title, description):
    embed = Embed(
        None,
        description,
    )
    
    add_current_track_field(embed, player)
    add_song_selection_header(embed, title, user)
    
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
        title = track.title
        if len(title) > 50:
            title = title[:47]
            option_label_parts.append(title)
            option_label_parts.append('...')
        else:
            option_label_parts.append(title)
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
    
    add_current_track_field(embed, player)
    
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
    
    add_current_track_field(embed, player)
    
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
    
    queue_length = len(player.queue)
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
        
        add_song_selection_header(embed, 'Track selection', user)
        
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
        title_parts = []
        
        if (selected_track_index <= 0) or (selected_track_index >= length):
            if player is None:
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
                    length_truncated = -(TRACK_PER_PAGE-length)
                    length = TRACK_PER_PAGE
                else:
                    length_truncated = 0
                
                index = 0
                
                while True:
                    track = tracks[index]
                    emoji = emojis[index]
                    index += 1
                    description_parts.append(emoji.as_emoji)
                    description_parts.append(' **')
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
        if player is None:
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
    ).add_author(
        user.avatar_url,
        'Song selection | Please select the song(s) to play',
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
        ).add_author(
            user.avatar_url,
            'Song selection | Nothing was chosen',
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
        
        if player is None:
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
async def behavior_(client, event,
    behavior : (BEHAVIOR_CHOICES, 'Choose a behavior') = BEHAVIOR_VALUE_GET,
    value : (bool, 'Set value') = True,
):
    """Get or set the player's behavior."""
    player = client.solarlink.get_player(event.guild_id)

    if player is None:
        abort('There is no player at the guild.')
        return
    
    if behavior == BEHAVIOR_VALUE_GET:
        content = get_behavior_string(player)
    
    elif behavior == BEHAVIOR_VALUE_REPEAT_CURRENT:
        player.set_repeat_current(value)
        if value:
            content = 'Started to repeat the current track.'
        else:
            content = 'Stopped to repeat the current track.'
    
    elif behavior == BEHAVIOR_VALUE_REPEAT_QUEUE:
        player.set_repeat_queue(value)
        if value:
            content = 'Started to repeat the whole queue.'
        else:
            content = 'Stopped to repeat the whole queue.'
        
    elif behavior == BEHAVIOR_VALUE_SHUFFLE:
        player.set_shuffle(value)
        if value:
            content = 'Started shuffling the queue.'
        else:
            content = 'Stopped to shuffle the queue.'
    
    else:
        return # ?
    
    return content


def generate_track_autocomplete_form(configured_track):
    result = configured_track.track.title
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
    
    configured_track = await player.skip(index)
    if configured_track is None:
        return 'Nothing was skipped.'
    
    return create_added_music_embed(
        player,
        event.user,
        'Track skipped',
        create_track_short_description(configured_track),
    )


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
    
    return create_added_music_embed(
        player,
        event.user,
        'Track removed',
        create_track_short_description(configured_track),
    )


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
    page: (int, 'Which page to show?') = 1,
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
        limit_low = (page-1)*TRACK_PER_PAGE
        limit_high = limit_low+TRACK_PER_PAGE
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
                description_parts.append(track.emoji.as_emoji)
                description_parts.append(' ')
                add_track_short_description_to(description_parts, track)
                
                if index == limit_high:
                    break
                
                description_parts.append('\n')
                continue
            
            description = ''.join(description_parts)
        else:
            description = None
        
        embed = Embed(None, description)
        
        page_count = ceil(length/TRACK_PER_PAGE)
        embed.add_footer(f'Page {page} / {page_count}')
        
        add_current_track_field(embed, player)
        
        embed.add_field(
            f'{EMOJI_QUEUE_LENGTH} Queue length',
            (
                f'```\n'
                f'{length}\n'
                f'```'
            ),
            inline = True,
        )
        
        embed.add_field(
            f'{EMOJI_QUEUE_TIME} Queue duration',
            (
                f'```\n'
                f'{duration_to_string(player.queue_duration)}\n'
                f'```'
            ),
            inline = True,
        )
        
        voice_channel = player.channel
        if voice_channel is None:
            # not in cache
            voice_channel_name = '#unknown'
        else:
            voice_channel_name = voice_channel.name
        
        embed.add_field(
            f'{EMOJI_CHANNEL} Playing in',
            (
                f'```\n'
                f'{voice_channel_name}'
                f'```'
            )
        )
    
        embed.add_field(
            f'{EMOJI_BEHAVIOR} Behavior',
            (
                f'```\n'
                f'{get_behavior_string(player)}\n'
                f'```'
            ),
            inline = True
        )
        
        embed.add_field(
            f'{EMOJI_VOLUME} Volume',
            (
                f'```\n'
                f'{player.get_volume()*100.:.0f}%\n'
                f'```'
            ),
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


PERMISSION_MASK_MESSAGING = Permission().update_by_keys(
    send_messages = True,
    send_messages_in_threads = True,
)

@SLASH_CLIENT.events
async def track_end(client, event):
    if event.reason != TRACK_END_REASONS.finished:
        return
    
    player = event.player
    new_track = player.get_current()
    old_track = event.track
    if new_track is old_track:
        return
    
    text_channel = player.text_channel
    if (text_channel is None) or (not text_channel.cached_permissions_for(client)&PERMISSION_MASK_MESSAGING):
        return
    
    embed = Embed()
    
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
        text_channel,
        embed = embed,
    )
