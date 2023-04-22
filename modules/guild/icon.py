__all__ = ()

from hata import Client
from hata.ext.slash import abort

from bots import SLASH_CLIENT

from .base_command import GUILD_COMMANDS
from .constants import (
    CUSTOM_ID_GUILD_BANNER, CUSTOM_ID_GUILD_DISCOVERY_SPLASH, CUSTOM_ID_GUILD_ICON, CUSTOM_ID_GUILD_INVITE_SPLASH,
    ICON_KINDS, ICON_KIND_BANNER, ICON_KIND_DISCOVERY_SPLASH, ICON_KIND_ICON, ICON_KIND_INVITE_SPLASH
)
from .icon_helpers import build_icon_embed, build_icon_interaction_response, is_command_invoker_same


@GUILD_COMMANDS.interactions(name = 'icon')
async def guild_icon_slash_command(event,
    icon_kind: (ICON_KINDS, 'Which icon of the guild?', 'icon') = ICON_KIND_ICON,
):
    """Shows the guild's icon."""
    guild = event.guild
    if (guild is None) or guild.partial:
        abort('The command unavailable in guilds, where the application\'s bot is not in.')
    
    return build_icon_interaction_response(guild, icon_kind)


async def handle_button_click(client, event, icon_kind):
    """
    Handles an icon button click.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    icon_kind : `int`
        The icon kind to create response to.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    guild = event.guild
    if guild is None:
        return
    
    if is_command_invoker_same(event):
        return build_icon_interaction_response(guild, icon_kind)
    
    await client.interaction_component_acknowledge(event)
    await client.interaction_followup_message_create(
        event, embed = build_icon_embed(guild, icon_kind), show_for_invoking_user_only = True
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_GUILD_ICON)
async def handle_guild_icon(client, event):
    return await handle_button_click(client, event, ICON_KIND_ICON)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_GUILD_BANNER)
async def handle_guild_banner(client, event):
    return await handle_button_click(client, event, ICON_KIND_BANNER)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_GUILD_DISCOVERY_SPLASH)
async def handle_guild_discovery_splash(client, event):
    return await handle_button_click(client, event, ICON_KIND_DISCOVERY_SPLASH)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_GUILD_INVITE_SPLASH)
async def handle_guild_invite_splash(client, event):
    return await handle_button_click(client, event, ICON_KIND_INVITE_SPLASH)
