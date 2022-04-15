from hata.ext.slash import SlasherApplicationCommand
from hata.ext.extension_loader import import_extension


get_player_or_abort = import_extension('..helpers', 'get_player_or_abort')

COMMAND: SlasherApplicationCommand


@COMMAND.interactions
async def stop(client, event):
    """Nyahh, if you really want I can stop playing audio."""
    player = get_player_or_abort(client, event)

    await player.stop()
    return 'Stopped playing'
