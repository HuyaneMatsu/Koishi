__all__ = ('resume_', )

from hata import Embed

from ..constants import EMBED_COLOR
from ..helpers import add_current_track_field, get_player_or_abort


async def resume_(client, event):
    """Resumes the currently playing track."""
    player = get_player_or_abort(client, event)
    
    if player.is_paused():
        await player.resume()
        title = 'Playing resumed.'
    else:
        title = 'Playing resumed. (was not paused before)'
    
    embed = Embed(
        title,
        color = EMBED_COLOR,
    )
    
    add_current_track_field(embed, player)
    
    return embed
