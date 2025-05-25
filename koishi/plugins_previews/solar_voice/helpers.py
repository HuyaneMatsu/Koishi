__all__ = ()

from math import floor
from hata import Embed, StringSelectOption, create_string_select, escape_markdown
from hata.ext.slash import abort

from .constants import EMOJI_CURRENT_TRACK, EMOJI_STOPPED, EMOJI_PLAYING, EMBED_COLOR, \
    LAVA_VOICE_TRACK_SELECT_CUSTOM_ID


def duration_to_string(duration):
    duration = int(duration)
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    
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
            string = 'Repeating and shuffling the queue.'
        else:
            string = 'Repeating over the queue.'
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


def get_behavior_representation(player):
    if player.is_repeating_queue():
        if player.is_shuffling():
            representation = 'repeat queue | shuffle'
        else:
            representation = 'repeat queue | no shuffle'
    elif player.is_repeating_current():
        if player.is_shuffling():
            representation = 'repeat current | shuffle'
        else:
            representation = 'repeat current | no shuffle'
    else:
        if player.is_shuffling():
            representation = 'no repeat | shuffle'
        else:
            representation = 'no repeat | no shuffle'
    
    return representation


def add_track_title_to(into, track):
    title = track.title
    if len(title) > 50:
        title = title[:47]
        title = escape_markdown(title)
        into.append(title)
        into.append('...')
    else:
        title = escape_markdown(title)
        into.append(title)


def add_track_duration_to(into, track):
    duration = int(track.duration)
    into.append('(')
    into.append(str(duration // 60))
    into.append(':')
    into.append(format(duration % 60, '0>2'))
    into.append(')')


def add_track_short_description_to(into, track):
    # Add title
    url = track.url
    
    if (url is not None):
        into.append('[')
    
    into.append('**')
    add_track_title_to(into, track)
    into.append('**')
    
    if (url is not None):
        into.append('](')
        into.append(url)
        into.append(')')
    
    into.append(' ')
    
    add_track_duration_to(into, track)



def create_track_short_description(configured_track):
    into = []
    into.append(configured_track.emoji.as_emoji)
    into.append(' ')
    add_track_short_description_to(into, configured_track.track)
    return ''.join(into)


def add_track_short_field_description_to(into, configured_track):
    into.append(configured_track.emoji.as_emoji)
    into.append(' ')
    
    add_track_short_description_to(into, configured_track.track)
    
    into.append('\n**Queued by:** ')
    
    # Add who queued it
    into.append(configured_track.requester.full_name)
    
    return configured_track


def create_track_short_field_description(configured_track):
    into = []
    add_track_short_field_description_to(into, configured_track)
    return ''.join(into)

def add_song_selection_header(embed, title, user):
    return embed.add_author(
        title,
        user.avatar_url,
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


def add_current_track_field_with_bar(embed, player):
    track = player.get_current()
    if (track is not None):
        if player.is_paused():
            title = 'paused'
            playing_emoji = EMOJI_STOPPED
        else:
            title = 'playing'
            playing_emoji = EMOJI_PLAYING
        
        into = []
        into.append(track.emoji.as_emoji)
        into.append(' ')
        url = track.url
        
        if (url is not None):
            into.append('[')
        
        into.append('**')
        add_track_title_to(into, track)
        into.append('**')
        
        if (url is not None):
            into.append('](')
            into.append(url)
            into.append(')')
        
        into.append('\n')
        into.append(playing_emoji.as_emoji)
        into.append(' 【')
        
        duration = track.duration
        position = player.position
        
        before = floor(19.0 * (position / duration))
        
        into.append('—'*before)
        into.append('⚪')
        into.append('—'*(19-before))
        into.append('】')
        
        duration = int(duration)
        position = int(position)
        
        into.append('(')
        into.append(str(position // 60))
        into.append(':')
        into.append(format(position % 60, '0>2'))
        into.append(' / ')
        into.append(str(duration // 60))
        into.append(':')
        into.append(format(duration % 60, '0>2'))
        into.append(')')
        
        embed.add_field(
            f'{EMOJI_CURRENT_TRACK} Currently {title}',
            ''.join(into),
        )
    
    return embed


def create_added_music_embed(player, user, title, description):
    embed = Embed(
        None,
        description,
        color = EMBED_COLOR,
    )
    
    add_current_track_field(embed, player)
    add_song_selection_header(embed, title, user)
    
    return embed



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
        
        options.append(StringSelectOption(option_value, option_label))
        
        if index == length:
            break
    
    return create_string_select(
        options,
        LAVA_VOICE_TRACK_SELECT_CUSTOM_ID,
        placeholder = 'Select a track to play',
        max_values = length,
    )


def get_player_or_abort(client, event):
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('There is no player at the guild.')
    
    return player
