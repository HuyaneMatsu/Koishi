__all__ = ()

from datetime import datetime as DateTime

from dateutil.relativedelta import relativedelta
from hata import Color, DATETIME_FORMAT_CODE, Embed, elapsed_time


USER_COLOR_JOIN = Color.from_rgb(2, 168, 77)
USER_COLOR_LEAVE = Color.from_rgb(168, 49, 2)

def render_created_into(into, user):
    """
    Renders the `created_at` field.
    
    Parameters
    ----------
    into : `list` of `str`
        List of strings to render the field into.
    user : ``ClientUserBase``
        The user to get the creation time of.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Created: ')
    into.append(format(user.created_at, DATETIME_FORMAT_CODE))
    return into


def render_profile_into(into, user):
    """
    Renders the user's profile (actually just a mention).
    
    Parameters
    ----------
    into : `list` of `str`
        List of strings to render the field into.
    user : ``ClientUserBase``
        The user to get the profile of.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Profile: ')
    into.append(user.mention)
    return into


def render_id_into(into, user):
    """
    Renders the user's identifier.
    
    Parameters
    ----------
    into : `list` of `str`
        List of strings to render the field into.
    user : ``ClientUserBase``
        The user to get their identifier of.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('ID: ')
    into.append(str(user.id))
    return into


def render_guild_profile_flags_into(into, guild_profile):
    """
    Renders the user's guild profile's flags.
    
    Parameters
    ----------
    into : `list` of `str`
        List of strings to render the field into.
    guild_profile : `None`, ``GuildProfile``
        The user guild profile if any.
    
    Returns
    -------
    into : `list` of `str`
    """
    if guild_profile is None:
        flags = 0
    else:
        flags = guild_profile.flags
    
    into.append('Flags: ')
    if flags:
        into.append(', '.join(flags).replace('_', ' '))
    else:
        into.append('*none*')
    
    return into


def render_joined_into(into, guild_profile, join):
    """
    Renders when the user joined the guild.
    
    Parameters
    ----------
    into : `list` of `str`
        List of strings to render the field into.
    guild_profile : `None`, ``GuildProfile``
        The user guild profile if any.
    join : `bool`
        Whether we are rendering a `join` event.
    
    Returns
    -------
    into : `list` of `str`
    """
    if guild_profile is None:
        joined_at = None
    else:
        joined_at = guild_profile.joined_at
    
    if joined_at is None:
        joined_text = 'Lurking since'
        if join:
            joined_at = DateTime.utcnow()
    else:
        joined_text = 'Joined at'
    
    if (joined_at is None):
        joined_at_string = 'N/A'
    else:
        joined_at_string = format(joined_at, DATETIME_FORMAT_CODE)
    
    into.append(joined_text)
    into.append(': ')
    into.append(joined_at_string)
    
    return into


def render_created_joined_difference_into(into, user, guild_profile, join):
    """
    Renders when the user's created - joined difference.
    
    Parameters
    ----------
    into : `list` of `str`
        List of strings to render the field into.
    user : ``ClientUserBase``
        The user to get their creation time.
    guild_profile : `None`, ``GuildProfile``
        The user guild profile if any.
    join : `bool`
        Whether we are rendering a `join` event.
    
    Returns
    -------
    into : `list` of `str`
    """
    if guild_profile is None:
        if join:
            joined_at = DateTime.utcnow()
        else:
            joined_at = None
    else:
        joined_at = guild_profile.joined_at
    
    if joined_at is None:
        difference_string = 'N/A'
    else:
        difference_string = elapsed_time(relativedelta(user.created_at, joined_at))
        
    into.append('Created - joined difference: ')
    into.append(difference_string)
    
    return into


def render_joined_left_difference_into(into, guild_profile):
    """
    Renders when the user's joined - left difference.
    
    > Only applicable when rendering a `leave` event.
    
    Parameters
    ----------
    into : `list` of `str`
        List of strings to render the field into.
    guild_profile : `None`, ``GuildProfile``
        The user guild profile if any.
    
    Returns
    -------
    into : `list` of `str`
    """
    if guild_profile is None:
        joined_at = None
    else:
        joined_at = guild_profile.joined_at
        
    if joined_at is None:
        difference_string = 'N/A'
    else:
        difference_string = elapsed_time(joined_at)
    
    into.append('Joined - left difference: ')
    into.append(difference_string)
    
    return into


def render_nick_into(into, guild_profile):
    """
    Renders the user's nick name.
    
    > Only applicable when rendering a `leave` event.
    
    Parameters
    ----------
    into : `list` of `str`
        List of strings to render the field into.
    guild_profile : `None`, ``GuildProfile``
        The user guild profile if any.
    
    Returns
    -------
    into : `list` of `str`
    """
    if guild_profile is None:
        nick = None
    else:
        nick = guild_profile.nick
    
    
    if nick is None:
        nick_string = '*none*'
    else:
        nick_string = nick
    
    into.append('Nick: ')
    into.append(nick_string)
    
    return into


def render_role_mentions_into(into, guild_profile):
    """
    Renders the user's roles.
    
    > Only applicable when rendering a `leave` event.
    
    Parameters
    ----------
    into : `list` of `str`
        List of strings to render the field into.
    guild_profile : `None`, ``GuildProfile``
        The user guild profile if any.
    
    Returns
    -------
    into : `list` of `str`
    """
    if guild_profile is None:
        roles = None
    else:
        roles = guild_profile.roles
    
    into.append('Roles: ')
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


def build_user_embed(guild, user, guild_profile, join):
    """
    Builds a user join or leave embed.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    user : ``ClientUserBase``
        The user who joined or left.
    guild_profile : `None`, ``GuildProfile``
        The user's guild profile in the guild.
    join : `bool`
        Whether the user joined or left.
    
    Returns
    -------
    embed : ``Embed``
    """
    description_parts = []
    
    render_profile_into(description_parts, user)
    description_parts.append('\n')
    render_id_into(description_parts, user)
    description_parts.append('\n')
    render_guild_profile_flags_into(description_parts, guild_profile)
    if not join:
        description_parts.append('\n')
        render_nick_into(description_parts, guild_profile)
        description_parts.append('\n')
        render_role_mentions_into(description_parts, guild_profile)
    
    
    description_parts.append('\n\n')
    render_created_into(description_parts, user)
    description_parts.append('\n')
    render_joined_into(description_parts, guild_profile, join)
    description_parts.append('\n')
    render_created_joined_difference_into(description_parts, user, guild_profile, join)
    if not join:
        description_parts.append('\n')
        render_joined_left_difference_into(description_parts, guild_profile)
    
    
    description = ''.join(description_parts)
    description_parts = None
    
    return Embed(
        user.full_name,
        description,
        color = (USER_COLOR_JOIN if join else USER_COLOR_LEAVE),
    ).add_thumbnail(
        user.avatar_url,
    ).add_author(
        f'User {"joined" if join else "left"} {guild.name}'
    )

