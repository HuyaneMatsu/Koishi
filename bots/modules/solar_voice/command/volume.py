from hata.ext.slash import SlasherApplicationCommand, P
from hata.ext.extension_loader import import_extension


EMOJI_VOLUME = import_extension('..constants', 'EMOJI_VOLUME')
get_player_or_abort = import_extension('..helpers', 'get_player_or_abort')


COMMAND: SlasherApplicationCommand


@COMMAND.interactions
async def volume_(client, event,
    volume: P('number', 'Percentage?', min_value=0, max_value=200) = None,
):
    """Gets or sets my volume to the given percentage."""
    player = get_player_or_abort(client, event)
    
    if volume is None:
        volume = player.get_volume()
        return f'{EMOJI_VOLUME.as_emoji} Volume: {volume * 100.:.0f}%'
    
    await player.set_volume(volume/100)
    return f'{EMOJI_VOLUME.as_emoji} Volume set to: {volume}%.'
