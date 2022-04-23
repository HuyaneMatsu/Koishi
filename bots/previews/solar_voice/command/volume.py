__all__ = ('volume_',)

from hata.ext.slash import P

from ..constants import EMOJI_VOLUME
from ..helpers import get_player_or_abort


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
