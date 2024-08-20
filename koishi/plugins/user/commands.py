__all__ = ()

from hata import ClientUserBase, Embed
from hata.ext.slash import Button, InteractionResponse, Row

from ...bots import FEATURE_CLIENTS

from .constants import (
    ICON_KIND_AVATAR, ICON_KIND_BANNER, ICON_SOURCE_CHOICES_AVATAR, ICON_SOURCE_CHOICES_BANNER, ICON_SOURCE_GLOBAL,
    ICON_SOURCE_GUILD, ICON_SOURCE_LOCAL
)
from .embed_builders import build_user_icon_embed, build_user_info_embed


USER_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    name = 'user',
    description = 'User commands',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)


@USER_COMMANDS.interactions(name = 'avatar')
async def user_avatar_command(
    event,
    user : (ClientUserBase, 'Choose a user!') = None,
    icon_source : (ICON_SOURCE_CHOICES_AVATAR, 'Which avatar of the user?', 'type') = ICON_SOURCE_LOCAL,
):
    """
    Shows your or the chosen user's avatar.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    user : `None | ClientUserBase` = `None`, Optional
        The user to get its avatar of.
    icon_source : `int` = `ICON_SOURCE_LOCAL`, Optional
        Icon source to show.
    
    Returns
    -------
    response : ``Embed``
    """
    if user is None:
        user = event.user
    
    return build_user_icon_embed(user, event.guild_id, ICON_KIND_AVATAR, icon_source)


@USER_COMMANDS.interactions(name = 'banner')
async def user_banner_command(
    client,
    event,
    user : (ClientUserBase, 'Choose a user!') = None,
    icon_source : (ICON_SOURCE_CHOICES_BANNER, 'Which banner of the user?', 'type') = ICON_SOURCE_LOCAL,
):
    """
    Shows your or the chosen user's banner.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    user : `None | ClientUserBase` = `None`, Optional
        The user to get its banner of.
    icon_source : `int` = `ICON_SOURCE_LOCAL`, Optional
        Icon source to show.
    
    Yields
    -------
    response : `None | Embed
    """
    if user is None:
        user = event.user
    
    yield
    
    await client.user_get(user, force_update = True)
    
    yield build_user_icon_embed(user, event.guild_id, ICON_KIND_BANNER, icon_source)


@USER_COMMANDS.interactions(name = 'info')
async def user_info_command(
    event,
    user: (ClientUserBase, 'Check out someone other user?') = None,
):
    """
    Shows some information about your or about the selected user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    user : `None | ClientUserBase` = `None`, Optional
        They targeted user.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if user is None:
        user = event.user
    
    embed = build_user_info_embed(user, event.guild_id)
    
    if user.get_guild_profile_for(event.guild_id) is None:
        components = Row(
            Button('Show avatar', custom_id = f'user.info.{user.id}.{ICON_KIND_AVATAR}.{ICON_SOURCE_GLOBAL}'),
            Button('Show banner', custom_id = f'user.info.{user.id}.{ICON_KIND_BANNER}.{ICON_SOURCE_GLOBAL}'),
        )
    else:
        components = Row(
            Button('Show global avatar', custom_id = f'user.info.{user.id}.{ICON_KIND_AVATAR}.{ICON_SOURCE_GLOBAL}'),
            Button('Show guild avatar', custom_id = f'user.info.{user.id}.{ICON_KIND_AVATAR}.{ICON_SOURCE_GUILD}'),
            Button('Show global banner', custom_id = f'user.info.{user.id}.{ICON_KIND_BANNER}.{ICON_SOURCE_GLOBAL}'),
            Button('Show guild banner', custom_id = f'user.info.{user.id}.{ICON_KIND_BANNER}.{ICON_SOURCE_GUILD}'),
        )
    
    return InteractionResponse(embed = embed, components = components)
