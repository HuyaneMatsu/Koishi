__all__ = ('leave_',)

from hata import Embed

from ..constants import EMBED_COLOR, EMOJI_CURRENT_TRACK
from ..helpers import create_track_short_field_description, get_player_or_abort


async def leave_(client, event):
    """Leaves from the voice channel."""
    player = get_player_or_abort(client, event)
    
    yield
    await player.disconnect()
    
    title =  f'{client.name_at(event.guild)} out.'
    
    embed = Embed(
        title,
        color = EMBED_COLOR,
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
