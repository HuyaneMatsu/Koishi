__all__ = ()

import re
from datetime import datetime as DateTime

from hata import Client, DATETIME_FORMAT_CODE, Embed, User, elapsed_time
from hata.ext.slash import Button, InteractionResponse, Row


SLASH_CLIENT : Client


ICON_TYPE_AVATAR = 1
ICON_TYPE_BANNER = 2

ICON_SOURCE_LOCAL = 1
ICON_SOURCE_GLOBAL = 2
ICON_SOURCE_GUILD = 3
ICON_SOURCE_DEFAULT = 4

ICON_TYPES_RP_GROUP = f'({ICON_TYPE_AVATAR}|{ICON_TYPE_BANNER})'
ICON_SOURCE_RP_GROUP = f'({ICON_SOURCE_LOCAL}|{ICON_SOURCE_GLOBAL}|{ICON_SOURCE_GUILD}|{ICON_SOURCE_DEFAULT})'


ICON_SOURCES = {
    'local' : ICON_SOURCE_LOCAL,
    'guild': ICON_SOURCE_GUILD,
    'global': ICON_SOURCE_GLOBAL,
    'default': ICON_SOURCE_DEFAULT,
}

ICON_SOURCES_REVERSED = {value: key for key, value in ICON_SOURCES.items()}

ICON_TYPES = {
    'avatar': ICON_TYPE_AVATAR,
    'banner': ICON_TYPE_BANNER,
}

ICON_TYPES_REVERSED = {value: key for key, value in ICON_TYPES.items()}


def get_avatar_of(user, guild_id, icon_source):
    """
    Gets the avatar url of the user in the given context.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    guild_id : `int`
        The context's guild's identifier.
    icon_source : `int`
        From which source should be the icon taken from.
    
    Returns
    -------
    icon_url : `None`, `str`
    """
    if icon_source == ICON_SOURCE_LOCAL:
        icon_url = user.avatar_url_at_as(guild_id, size = 4096)
    
    elif icon_source == ICON_SOURCE_GLOBAL:
        icon_url = user.avatar_url_as(size = 4096)
    
    elif icon_source == ICON_SOURCE_GUILD:
        icon_url = user.avatar_url_for_as(guild_id, size = 4096)
    
    elif icon_source == ICON_SOURCE_DEFAULT:
        icon_url = user.default_avatar_url
        
    else:
        icon_url = None
    
    return icon_url


def get_banner_of(user, guild_id, icon_source):
    """
    Gets the banner url of the user in the given context.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    guild_id : `int`
        The context's guild's identifier.
    icon_source : `int`
        From which source should be the icon taken from.
    
    Returns
    -------
    icon_url : `None`, `str`
    """
    if icon_source == ICON_SOURCE_GLOBAL:
        icon_url = user.banner_url_as(size = 4096)
    
    else:
        icon_url = None
        
    return icon_url


def get_icon_of(user, guild_id, icon_type, icon_source):
    """
    Gets the defined icon url of the user in the given context.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    guild_id : `int`
        The context's guild's identifier.
    icon_type : `int`
        Which icon should be taken of the user.
    icon_source : `int`
        From which source should be the icon taken from.
    
    Returns
    -------
    icon_url : `None`, `str`
    """
    if icon_type == ICON_TYPE_AVATAR:
        return get_avatar_of(user, guild_id, icon_source)
    
    if icon_type == ICON_TYPE_BANNER:
        return get_banner_of(user, guild_id, icon_source)
    
    return None


def put_roles_into(roles, into):
    """
    Puts the given roles representation into the given string container. 
    
    Parameters
    ----------
    roles : `None`, `tuple` of ``Role``
        Date time to convert.
    into : `list` of `str`
        Container.
    
    Returns
    -------
    into : `list` of `str`
    """
    if roles is None:
        into.append('*none*')
    
    else:
        roles_reversed = [*reversed(roles)]
        
        length = len(roles_reversed)
        if length > 20:
            removed = length - 20
            length = 20
            del roles_reversed[20:]
        
        else:
            removed = 0
        
        index = 0
        
        while True:
            role = roles_reversed[index]
            into.append(role.mention)
            
            index += 1
            if index == length:
                break
            
            into.append(', ')
            continue
        
        if removed:
            into.append(', ... +')
            into.append(str(removed))
        
    return into


def put_date_time_into(date_time, into, add_ago):
    """
    Puts the given date time's string value into the given string container. 
    
    Parameters
    ----------
    date_time : `None`, `DateTime`
        Date time to convert.
    into : `list` of `str`
        Container.
    add_ago : `bool`
        Whether ago should be added to teh relative representation.
    
    Returns
    -------
    into : `list` of `str`
    """
    if date_time is None:
        into.append('*none*')
    
    else:
        into.append(format(date_time, DATETIME_FORMAT_CODE))
        into.append(' [*')
        into.append(elapsed_time(date_time))
        into.append(' ')
        if add_ago:
            into.append('ago')
        into.append('*]')
    
    return into


def add_user_info_embed_field(embed, user):
    """
    Adds user info field to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to add the field to.
    user : ``ClientUserBase``
        The respective user.
    
    Returns
    -------
    embed : ``Embed``
    """
    value_parts = ['Created: ']
    put_date_time_into(user.created_at, value_parts, True)
    value_parts.append('\nID:')
    value_parts.append(str(user.id))
    
    return embed.add_field('User Information', ''.join(value_parts))


def add_user_guild_profile_info_embed_field(embed, guild_profile):
    """
    Adds user guild profile info field to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to add the field to.
    guild_profile : ``GuildProfile``
        The user's guild profile.
    
    Returns
    -------
    embed : ``Embed``
    """
    value_parts = ['Joined: ']
    put_date_time_into(guild_profile.joined_at, value_parts, True)
    value_parts.append('\nRoles: ')
    put_roles_into(guild_profile.roles, value_parts)
    
    nick = guild_profile.nick
    if (nick is not None):
        value_parts.append('\nNick: ')
        value_parts.append(nick)
    
    
    boosts_since = guild_profile.boosts_since
    if (boosts_since is not None):
        value_parts.append('\nBooster since: ')
        put_date_time_into(boosts_since, value_parts, False)
    
    
    timed_out_until = guild_profile.timed_out_until
    if (timed_out_until is not None) and (timed_out_until > DateTime.utcnow()):
        value_parts.append('\nTimed out until: ')
        put_date_time_into(timed_out_until, value_parts, False)
    
    return embed.add_field('In guild profile', ''.join(value_parts))


USER_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'user',
    description = 'User commands',
    is_global = True,
)


@USER_COMMANDS.interactions
async def info(
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
            Button('Show avatar', custom_id = f'user.info.{user.id}.{ICON_TYPE_AVATAR}.{ICON_SOURCE_GLOBAL}'),
            Button('Show banner', custom_id = f'user.info.{user.id}.{ICON_TYPE_BANNER}.{ICON_SOURCE_GLOBAL}'),
        )
    
    else:
        embed.color = user.color_at(guild)
        add_user_guild_profile_info_embed_field(embed, guild_profile)
        
        components = Row(
            Button('Show global avatar', custom_id = f'user.info.{user.id}.{ICON_TYPE_AVATAR}.{ICON_SOURCE_GLOBAL}'),
            Button('Show guild avatar', custom_id = f'user.info.{user.id}.{ICON_TYPE_AVATAR}.{ICON_SOURCE_GUILD}'),
            Button('Show banner', custom_id = f'user.info.{user.id}.{ICON_TYPE_BANNER}.{ICON_SOURCE_GLOBAL}'),
        )
    
    return InteractionResponse(embed = embed, components = components)


@SLASH_CLIENT.interactions(custom_id = re.compile(f'user\.info\.(\d+)\.{ICON_TYPES_RP_GROUP}\.{ICON_SOURCE_RP_GROUP}'))
async def show_user_icon(client, event, user_id, icon_type, icon_source):
    user_id = int(user_id)
    icon_type = int(icon_type)
    icon_source = int(icon_source)
    
    yield
    
    user = await client.user_get(user_id, force_update = True)
    
    icon_url = get_icon_of(user, event.guild_id, icon_type, icon_source)
    
    embed = Embed(
        f'{user:f}\'s {ICON_SOURCES_REVERSED[icon_source]} {ICON_TYPES_REVERSED[icon_type]}',
        url = icon_url,
        color = (event.id >> 22) & 0xffffff,
    )
    
    if icon_url is None:
        embed.add_footer(
            f'The user has no {ICON_SOURCES_REVERSED[icon_source]} {ICON_TYPES_REVERSED[icon_type]}.',
        )
    else:
        embed.add_image(
            icon_url,
        )
    
    await client.interaction_followup_message_create(event, embed = embed, show_for_invoking_user_only = True)


@USER_COMMANDS.interactions
async def avatar(
    event,
    user : (User, 'Choose a user!') = None,
    icon_source : (ICON_SOURCES, 'Which avatar of the user?', 'type') = ICON_SOURCES,
):
    """Shows your or the chosen user's avatar."""
    if user is None:
        user = event.user
    
    icon_url = get_avatar_of(user, event.guild_id, icon_source)
    if icon_url is None:
        icon_url = user.default_avatar_url
    
    return Embed(
        f'{user:f}\'s {ICON_SOURCES_REVERSED[icon_source]} avatar',
        color = (event.id >> 22) & 0xffffff,
        url = icon_url,
    ).add_image(
        icon_url,
    )
