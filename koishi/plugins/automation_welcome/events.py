__all__ = ()

from random import choice

from hata import Client

from ...bots import SLASH_CLIENT

from ..automation_core import get_welcome_channel

from .constants import WELCOME_MESSAGES


@SLASH_CLIENT.events
async def guild_user_add(client, guild, user):
    """
    Handles a guild user add event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild the user has been added to.
    user : ``ClientUserBase``
        The added user.
    """
    channel = get_welcome_channel(guild.id)
    if (channel is None):
        return
    
    await client.message_create(
        channel,
        content = choice(WELCOME_MESSAGES)(user),
        silent = True,
    )
