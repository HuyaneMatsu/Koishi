__all__ = ()

from ...bots import FEATURE_CLIENTS

from ..stats_core import get_stats

from .embed_builders import build_stats_embed


STAT_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    name = 'stats',
    description = 'Wanna know you stats?',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)


@STAT_COMMANDS.interactions
async def show(
    event,
    user: ('user', 'Select someone else?') = None,
):
    """
    Shows your waifu stats.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    user : `None`, ``ClientUserBase`` = `None`, Optional
        The selected user.
    
    Returns
    -------
    response : ``Embed``
    """
    if user is None:
        user = event.user
    
    stats = await get_stats(user.id)
    return build_stats_embed(stats, user, event.guild_id)
