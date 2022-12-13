__all__ = ()

import re

from hata import Client, Embed, User
from hata.ext.slash import Button, InteractionResponse, Row

from .constants import (
    ICON_SOURCES_REVERSED, ICON_SOURCE_GLOBAL, ICON_SOURCE_GUILD, ICON_SOURCE_RP_GROUP, ICON_KINDS_REVERSED,
    ICON_KINDS_RP_GROUP, ICON_KIND_AVATAR, ICON_KIND_BANNER
)
from .icon_helpers import get_icon_of
from .info_helpers import add_user_guild_profile_info_embed_field, add_user_info_embed_field


SLASH_CLIENT : Client


async def user_info_command(
    event,
    user: (User, 'Check out someone other user?') = None,
):
    """Shows some information about your or about the selected user."""
    if user is None:
        user = event.user
    
    guild = event.guild
    
    embed = Embed(
        user.full_name,
    ).add_thumbnail(
        user.avatar_url,
    )
    
    add_user_info_embed_field(embed, user)
    
    guild_profile = user.get_guild_profile_for(guild)
    
    if guild_profile is None:
        embed.color = (user.id >> 22) & 0xffffff
        components = Row(
            Button('Show avatar', custom_id = f'user.info.{user.id}.{ICON_KIND_AVATAR}.{ICON_SOURCE_GLOBAL}'),
            Button('Show banner', custom_id = f'user.info.{user.id}.{ICON_KIND_BANNER}.{ICON_SOURCE_GLOBAL}'),
        )
    
    else:
        embed.color = user.color_at(guild)
        add_user_guild_profile_info_embed_field(embed, guild_profile)
        
        components = Row(
            Button('Show global avatar', custom_id = f'user.info.{user.id}.{ICON_KIND_AVATAR}.{ICON_SOURCE_GLOBAL}'),
            Button('Show guild avatar', custom_id = f'user.info.{user.id}.{ICON_KIND_AVATAR}.{ICON_SOURCE_GUILD}'),
            Button('Show banner', custom_id = f'user.info.{user.id}.{ICON_KIND_BANNER}.{ICON_SOURCE_GLOBAL}'),
        )
    
    return InteractionResponse(embed = embed, components = components)


@SLASH_CLIENT.interactions(custom_id = re.compile(f'user\.info\.(\d+)\.{ICON_KINDS_RP_GROUP}\.{ICON_SOURCE_RP_GROUP}'))
async def show_user_icon(client, event, user_id, icon_kind, icon_source):
    user_id = int(user_id)
    icon_kind = int(icon_kind)
    icon_source = int(icon_source)
    
    yield
    
    user = await client.user_get(user_id, force_update = True)
    
    icon_url = get_icon_of(user, event.guild_id, icon_kind, icon_source)
    
    embed = Embed(
        f'{user:f}\'s {ICON_SOURCES_REVERSED[icon_source]} {ICON_KINDS_REVERSED[icon_kind]}',
        url = icon_url,
        color = (event.id >> 22) & 0xffffff,
    )
    
    if icon_url is None:
        embed.add_footer(
            f'The user has no {ICON_SOURCES_REVERSED[icon_source]} {ICON_KINDS_REVERSED[icon_kind]}.',
        )
    else:
        embed.add_image(
            icon_url,
        )
    
    await client.interaction_followup_message_create(event, embed = embed, show_for_invoking_user_only = True)
