from hata import Embed
from hata.ext.slash import SlasherApplicationCommand
from hata.ext.extension_loader import import_extension


EMBED_COLOR = import_extension('..constants', 'EMBED_COLOR')
add_current_track_field, get_player_or_abort = import_extension(
    '..helpers', 'add_current_track_field', 'get_player_or_abort'
)

COMMAND: SlasherApplicationCommand


@COMMAND.interactions
async def resume(client, event):
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
