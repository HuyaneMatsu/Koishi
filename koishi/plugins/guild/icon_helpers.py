__all__ = ()

from hata import Embed, ICON_TYPE_NONE
from hata.ext.slash import Button, InteractionResponse, Row

from .constants import (
    CUSTOM_ID_GUILD_BANNER, CUSTOM_ID_GUILD_DISCOVERY_SPLASH, CUSTOM_ID_GUILD_ICON, CUSTOM_ID_GUILD_INVITE_SPLASH,
    ICON_KINDS_REVERSED, ICON_KIND_BANNER, ICON_KIND_DISCOVERY_SPLASH, ICON_KIND_ICON, ICON_KIND_INVITE_SPLASH
)


GUILD_ICON_URL_GETTERS = {
    ICON_KIND_ICON: (lambda guild: guild.icon_url_as(size = 4096)),
    ICON_KIND_BANNER: (lambda guild: guild.banner_url_as(size = 4096)),
    ICON_KIND_DISCOVERY_SPLASH: (lambda guild: guild.discovery_splash_url_as(size = 4096)),
    ICON_KIND_INVITE_SPLASH: (lambda guild: guild.invite_splash_url_as(size = 4096)),
}


GUILD_ICON_HASH_GETTERS = {
    ICON_KIND_ICON: (lambda guild: guild.icon_hash),
    ICON_KIND_BANNER: (lambda guild: guild.banner_hash),
    ICON_KIND_DISCOVERY_SPLASH: (lambda guild: guild.discovery_splash_hash),
    ICON_KIND_INVITE_SPLASH: (lambda guild: guild.invite_splash_hash),
}


def should_be_enabled(icon_type, local, current):
    """
    Returns whether the given icon should be enabled.
    
    Parameters
    ----------
    icon_type : ``IconType``
        The icon's type.
    local : `int`
        The local icon's kind.
    current : `int`
        The currently selected icon's kind.
    """
    if icon_type is ICON_TYPE_NONE:
        return False
    
    if local == current:
        return False
    
    return True


def build_icon_components(guild, current):
    """
    Builds icon select components for the given guild.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    current : `int`
        The currently selected icon's kind.
    
    Returns
    -------
    components : ``Component``
    """
    return Row(
        Button(
            'Icon',
            custom_id = CUSTOM_ID_GUILD_ICON,
            enabled = should_be_enabled(guild.icon_type, ICON_KIND_ICON, current),
        ),
        Button(
            'Banner',
            custom_id = CUSTOM_ID_GUILD_BANNER,
            enabled = should_be_enabled(guild.banner_type, ICON_KIND_BANNER, current),
        ),
        Button(
            'Discovery-splash',
            custom_id = CUSTOM_ID_GUILD_DISCOVERY_SPLASH,
            enabled = should_be_enabled(guild.discovery_splash_type, ICON_KIND_DISCOVERY_SPLASH, current),
        ),
        Button(
            'Invite-splash',
            custom_id = CUSTOM_ID_GUILD_INVITE_SPLASH,
            enabled = should_be_enabled(guild.invite_splash_type, ICON_KIND_INVITE_SPLASH, current),
        ),
    )


def build_icon_embed(guild, icon_kind):
    """
    Creates a guild icon embed.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    icon_kind : `int`
        The icon's kind.
    
    Returns
    -------
    embed : ``Embed``
    """
    icon_url = GUILD_ICON_URL_GETTERS[icon_kind](guild)
    name = ICON_KINDS_REVERSED[icon_kind]
    
    if icon_url is None:
        color = (guild.id >> 22) & 0xffffff
        embed = Embed(f'{guild.name} has no {name}', color = color)
    else:
        color = GUILD_ICON_HASH_GETTERS[icon_kind](guild) & 0xffffff
        embed = Embed(f'{guild.name}\'s {name}', color = color, url = icon_url).add_image(icon_url)
    
    return embed


def build_icon_interaction_response(guild, icon_kind):
    """
    Builds icon interaction response.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    icon_kind : `int`
        The icon's kind.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    return InteractionResponse(
        components = build_icon_components(guild, icon_kind),
        embed = build_icon_embed(guild, icon_kind),
    )


def is_command_invoker_same(event):
    """
    Returns whether the event's user is same as the command's invoker.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    is_command_invoker_same : `bool`
    """
    message = event.message
    if message is None:
        return False
    
    interaction = message.interaction
    if interaction is None:
        return False
    
    if interaction.user_id != event.user_id:
        return False
    
    return True
