__all__ = ('stop_', )

from ..helpers import get_player_or_abort


async def stop_(client, event):
    """Nyahh, if you really want I can stop playing audio."""
    player = get_player_or_abort(client, event)

    await player.stop()
    return 'Stopped playing'
