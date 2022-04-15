from hata import Embed
from hata.ext.slash import SlasherApplicationCommand, abort
from hata.ext.extension_loader import import_extension


EMBED_COLOR = import_extension('..constants', 'EMBED_COLOR')
add_current_track_field, get_player_or_abort = import_extension(
    '..helpers', 'add_current_track_field', 'get_player_or_abort'
)

COMMAND: SlasherApplicationCommand


@COMMAND.interactions
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
