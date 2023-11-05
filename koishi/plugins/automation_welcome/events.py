__all__ = ()

from hata import Embed, now_as_id
from hata.ext.slash import Button, ButtonStyle

from ...bots import SLASH_CLIENT

from ..automation_core import get_welcome_channel_and_button_enabled

from .constants import CUSTOM_ID_WELCOME_REPLY, ONBOARDING_MASK_ALL, ONBOARDING_MASK_STARTED
from .helpers import can_send_messages
from .welcome_styles import WELCOME_STYLE_DEFAULT


async def welcome_user(client, guild, user, welcome_style, welcome_channel, welcome_button_enabled):
    """
    Welcomes the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild the welcome the user at.
    user : ``ClientUserBase``
        The user to welcome.
    welcome_style : ``WelcomeStyle``
        The welcome style to use.
    welcome_channel : ``Channel``
        The channel to welcome the user at.
    welcome_button_enabled : `bool`
        Whether welcome reply button should be added under the message.
    """
    if not can_send_messages(welcome_channel, welcome_channel.cached_permissions_for(client)):
        return
    
    seed = guild.id ^ user.id
    
    message_content_builders = welcome_style.message_content_builders
    message_content = message_content_builders[seed % len(message_content_builders)](user.mention)
    
    images = welcome_style.images
    image = images[seed % len(images)]
    
    color = (now_as_id() >> 22) & 0xffffff
    
    if welcome_button_enabled:
        button_contents = welcome_style.button_contents
        button_content = button_contents[seed % len(button_contents)]
        welcome_button = Button(
            button_content, welcome_style.button_emoji, custom_id = CUSTOM_ID_WELCOME_REPLY, style = ButtonStyle.green
        )
    else:
        welcome_button = None
    
    await client.message_create(
        welcome_channel,
        components = welcome_button,
        content = f'> {message_content}',
        embed = Embed(color = color).add_image(image),
        silent = True,
    )


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
    welcome_channel, welcome_button_enabled = get_welcome_channel_and_button_enabled(guild.id)
    if (welcome_channel is None):
        return
    
    guild_profile = user.get_guild_profile_for(guild)
    if (guild_profile is None):
        flags = 0
    else:
        flags = guild_profile.flags
    
    # If onboarding is enabled, we probably do not want to send the welcome message
    if flags & ONBOARDING_MASK_ALL == ONBOARDING_MASK_STARTED:
        return
    
    # Send message
    await welcome_user(client, guild, user, WELCOME_STYLE_DEFAULT, welcome_channel, welcome_button_enabled)


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
    welcome_channel, welcome_button_enabled = get_welcome_channel_and_button_enabled(guild.id)
    if (welcome_channel is None):
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
    await welcome_user(client, guild, user, WELCOME_STYLE_DEFAULT, welcome_channel, welcome_button_enabled)
