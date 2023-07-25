__all__ = ()

from random import choice

from hata import Client

from ...bots import SLASH_CLIENT

from ..automation_core import get_welcome_channel

from .constants import ONBOARDING_MASK_ALL, ONBOARDING_MASK_STARTED, WELCOME_MESSAGES


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
    
    guild_profile = user.get_guild_profile_for(guild)
    if (guild_profile is None):
        flags = 0
    else:
        flags = guild_profile.flags
    
    # If onboarding is enabled, we probably do not want to send the welcome message
    if flags & ONBOARDING_MASK_ALL == ONBOARDING_MASK_STARTED:
        return
    
    await client.message_create(
        channel,
        content = choice(WELCOME_MESSAGES)(user),
        silent = True,
    )


@SLASH_CLIENT.events
async def guild_user_update(client, guild, user, old_attributes):
    """
    handles a guild user profile update event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild where the user's profile was updated at.
    user : ``ClientUserBase``
        The user who was updated.
    old_attributes : `None | dict<str, object>`
        The updated attributes.
    """
    channel = get_welcome_channel(guild.id)
    if (channel is None):
        return
    
    # Check whether the old flags are valid.
    if old_attributes is None:
        return
    
    try:
        old_flags = old_attributes['flags']
    except KeyError:
        return
    
    # The previous flags should have only onboarding started.
    if old_flags & ONBOARDING_MASK_ALL != ONBOARDING_MASK_STARTED:
        return
    
    # Check whether the new flags are valid.
    guild_profile = user.get_guild_profile_for(guild)
    if (guild_profile is None):
        new_flags = 0
    else:
        new_flags = guild_profile.flags
    
    # The new flags should have both.
    if new_flags & ONBOARDING_MASK_ALL != ONBOARDING_MASK_ALL:
        return
    
    # Send message
    await client.message_create(
        channel,
        content = choice(WELCOME_MESSAGES)(user),
        silent = True,
    )
