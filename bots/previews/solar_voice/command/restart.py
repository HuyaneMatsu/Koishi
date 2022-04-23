__all__ = ('restart_', )

from hata import Embed
from hata.ext.slash import abort

from ..constants import EMBED_COLOR
from ..helpers import add_current_track_field, get_player_or_abort


async def restart_(client, event):
    """Restarts the current track."""
    player = get_player_or_abort(client, event)
    
    track = player.get_current()
    if track is None:
        abort('The player is not playing anything.')
    
    await player.seek(0.0)

    embed = Embed('Track restarted.', color=EMBED_COLOR)
    add_current_track_field(embed, player)
    return embed
