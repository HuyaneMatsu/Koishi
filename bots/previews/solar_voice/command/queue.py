__all__ = ('queue_',)

from math import ceil

from hata import Embed

from ..constants import (
    EMBED_COLOR, EMOJI_BEHAVIOR, EMOJI_CHANNEL, EMOJI_QUEUE_LENGTH, EMOJI_QUEUE_TIME, EMOJI_VOLUME, TRACK_PER_PAGE
)
from ..helpers import (
    add_current_track_field_with_bar, add_track_short_description_to, duration_to_string, get_behavior_representation
)


async def queue_(client, event,
    page: (int, 'Which page to show?') = 1,
):
    """Shows the track queue for the current guild."""
    player = client.solarlink.get_player(event.guild_id)
    if player is None:
        embed = Embed(
            None,
            '**Once there were heart throbbing adventures, but now, one can find only dust and decay.**',
            color = EMBED_COLOR,
        )
    else:

        queue = player.queue
        length = len(queue)
        limit_low = (page - 1) * TRACK_PER_PAGE
        limit_high = limit_low + TRACK_PER_PAGE
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
        
        embed = Embed(None, description, color=EMBED_COLOR)
        
        page_count = ceil(length / TRACK_PER_PAGE)
        embed.add_footer(f'Page {page} / {page_count}')
        
        add_current_track_field_with_bar(embed, player)
        
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
                f'{get_behavior_representation(player)}\n'
                f'```'
            ),
            inline = True
        )
        
        embed.add_field(
            f'{EMOJI_VOLUME} Volume',
            (
                f'```\n'
                f'{player.get_volume() * 100.:.0f}%\n'
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
    
    embed.add_author(author_name, author_icon_url)
    return embed
