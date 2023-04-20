__all__ = ('pause_',)

from hata import Embed

from ..constants import EMBED_COLOR
from ..helpers import add_current_track_field, get_player_or_abort


async def pause_(client, event):
    """Pauses the currently playing track."""
    player = get_player_or_abort(client, event)
    
    if player.is_paused():
        title = 'Playing paused. (was paused before)'
    else:
        await player.pause()
        title = 'Playing paused.'
    
    embed = Embed(
        title,
        color = EMBED_COLOR,
    )
    
    add_current_track_field(embed, player)
    
    return embed
