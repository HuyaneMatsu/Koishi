__all__ = ()

from hata import Client

from ...bot_utils.multi_client_utils import get_first_client_with_message_create_permissions_from
from ...bots import FEATURE_CLIENTS

from ..automation_core import get_log_user_channel

from .embed_builder_user import build_user_embed


@FEATURE_CLIENTS.events
async def guild_user_add(client, guild, user):
    """
    Handles a guild user add event. If the guild has user logging setup, sends a message there.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The joined guild.
    user : ``ClientUserBase``
        The user who joined.
    """
    channel = get_log_user_channel(guild.id)
    if (channel is None):
        return
    
    if client is not get_first_client_with_message_create_permissions_from(channel, FEATURE_CLIENTS):
        return
    
    await client.message_create(
        channel,
        allowed_mentions = None,
        embed = build_user_embed(guild, user, user.get_guild_profile_for(guild), True),
    )


@FEATURE_CLIENTS.events
async def guild_user_delete(client, guild, user, guild_profile):
    """
    Handles a guild user delete event. If the guild has user logging setup, sends a message there.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The joined guild.
    user : ``ClientUserBase``
        The user who left.
    guild_profile : ``GuildProfile``
        The user's ex - guild profile at the guild.
    """
    channel = get_log_user_channel(guild.id)
    if (channel is None):
        return
    
    if client is not get_first_client_with_message_create_permissions_from(channel, FEATURE_CLIENTS):
        return
    
    # When the client itself is kicked it tries to log it, lets do that.
    if client is user:
        return
    
    await client.message_create(
        channel,
        allowed_mentions = None,
        embed = build_user_embed(guild, user, guild_profile, False),
    )
