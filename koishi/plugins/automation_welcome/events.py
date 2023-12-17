__all__ = ()

from hata import Embed, now_as_id
from hata.ext.slash import Button, ButtonStyle, Row

from ...bot_utils.multi_client_utils import get_first_client_with_message_create_permissions_from
from ...bots import FEATURE_CLIENTS

from ..automation_core import get_welcome_field
from ..embed_image_refresh import schedule_image_refresh

from .constants import (
    CUSTOM_ID_WELCOME_REPLY, CUSTOM_ID_WELCOME_REPLY_CUSTOM, ONBOARDING_MASK_ALL, ONBOARDING_MASK_STARTED
)
from .welcome_styles import get_welcome_style


async def welcome_user(client, guild, user, welcome_style, welcome_channel, welcome_reply_buttons_enabled):
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
    welcome_reply_buttons_enabled : `bool`
        Whether welcome reply button should be added under the message.
    """
    seed = guild.id ^ user.id
    
    message_content_builders = welcome_style.message_content_builders
    message_content = message_content_builders[seed % len(message_content_builders)](user.mention)
    
    images = welcome_style.images
    image = images[seed % len(images)]
    
    color = (now_as_id() >> 22) & 0xffffff
    
    if welcome_reply_buttons_enabled:
        reply_styles = welcome_style.reply_styles
        reply_style = reply_styles[seed % len(reply_styles)]
        
        welcome_reply_buttons = Row(
            Button(
                reply_style.button_content,
                reply_style.button_emoji,
                custom_id = CUSTOM_ID_WELCOME_REPLY,
                style = ButtonStyle.green,
            ),
            Button(
                'Your greeting',
                custom_id = CUSTOM_ID_WELCOME_REPLY_CUSTOM,
                style = ButtonStyle.green,
            )
        )
    else:
        welcome_reply_buttons = None
    
    message = await client.message_create(
        welcome_channel,
        components = welcome_reply_buttons,
        content = f'> {message_content}',
        embed = Embed(color = color).add_image(image),
        silent = True,
    )
    schedule_image_refresh(client, message)


@FEATURE_CLIENTS.events
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
    welcome_fields = get_welcome_field(guild.id)
    if (welcome_fields is None):
        return
    
    welcome_channel, welcome_reply_buttons_enabled, welcome_style_name = welcome_fields
    
    if client is not get_first_client_with_message_create_permissions_from(welcome_channel, FEATURE_CLIENTS):
        return
    
    guild_profile = user.get_guild_profile_for(guild)
    if (guild_profile is None):
        flags = 0
    else:
        flags = guild_profile.flags
    
    # If onboarding is enabled, we probably do not want to send the welcome message
    if flags & ONBOARDING_MASK_ALL == ONBOARDING_MASK_STARTED:
        return
    
    welcome_style = get_welcome_style(welcome_style_name, client.id)
    
    # Send message
    await welcome_user(client, guild, user, welcome_style, welcome_channel, welcome_reply_buttons_enabled)


@FEATURE_CLIENTS.events
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
    welcome_fields = get_welcome_field(guild.id)
    if (welcome_fields is None):
        return
    
    # Check whether the old flags are valid.
    if old_attributes is None:
        return
    
    welcome_channel, welcome_reply_buttons_enabled, welcome_style_name = welcome_fields
    
    if client is not get_first_client_with_message_create_permissions_from(welcome_channel, FEATURE_CLIENTS):
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
    
    welcome_style = get_welcome_style(welcome_style_name, client.id)
    
    # Send message
    await welcome_user(client, guild, user, welcome_style, welcome_channel, welcome_reply_buttons_enabled)
