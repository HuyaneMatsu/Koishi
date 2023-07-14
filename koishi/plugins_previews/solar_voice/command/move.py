__all__ = ('move_',)

from hata import Embed
from hata.ext.slash import abort

from ..constants import LEAVE_TIMEOUT
from ..helpers import get_player_or_abort


async def move_(client, event,
    channel: ('channel_group_connectable', 'Select a channel.'),
):
    """Moves me to the selected voice channel | You must have move users permission."""
    player = get_player_or_abort(client, event)
    
    if not event.user_permissions.can_move_users:
        abort('You must have move move users permission to invoke this command.')
    
    if not channel.cached_permissions_for(client).can_connect:
        abort(f'I have no permissions to connect to {channel.mention}.')
    
    
    yield
    
    moved = await player.move_to(channel)
    
    embed = Embed(
        None,
        f'Moved to {channel.mention}.'
    )
    
    if moved and player.check_auto_leave(channel.id):
        embed.add_footer(
            f'There are no users listening in {channel.name}. '
            f'I will leave from the channel after {LEAVE_TIMEOUT:.0f} seconds.'
        )
    
    yield embed
