__all__ = (
    'render_date_time_with_relative_into', 'render_flags_into', 'render_nullable_emoji_into',
    'render_nullable_string_tuple_into'
)

from hata import DATETIME_FORMAT_CODE, elapsed_time

from .constants import ROLE_MENTIONS_MAX, VOTERS_MAX


def render_role_mentions_into(into, roles):
    """
    Renders the given roles representation into the given string container. 
    
    Parameters
    ----------
    into : `list` of `str`
        Container.
    roles : `tuple` of ``Role``
        Date time to convert.
    
    Returns
    -------
    into : `list` of `str`
    """
    fields_added = 0
    
    for role in reversed(roles):
        if fields_added:
            into.append(', ')
        
        fields_added += 1
        
        if fields_added > ROLE_MENTIONS_MAX:
            into.append('... +')
            into.append(str(len(roles) - ROLE_MENTIONS_MAX))
            break
        
        into.append(role.mention)
        continue
    
    return into


def render_date_time_with_relative_into(into, date_time, add_ago):
    """
    Renders the given date time's string value into the given string container. 
    
    Parameters
    ----------
    into : `list` of `str`
        Container.
    date_time : `None | DateTime`
        Date time to convert.
    add_ago : `bool`
        Whether ago should be added to the relative representation.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(format(date_time, DATETIME_FORMAT_CODE))
    
    into.append(' [*')
    into.append(elapsed_time(date_time))
    if add_ago:
        into.append(' ago')
    into.append('*]')
    
    return into


def render_flags_into(into, flags):
    """
    Renders the given flags' representation onto the given list.
    
    Parameters
    ----------
    into : `list<str>`
        List to extend.
    
    flags : ``FlagBase``
        The flags to render.
    
    Returns
    -------
    into : `list<str>`
    """
    if not flags:
        into.append('*none*')
    
    else:
        field_added = False
        
        for flag_name in flags:
            if field_added:
                into.append(', ')
            else:
                field_added = True
            
            into.append(flag_name.replace('_', ' '))
    
    return into


def render_user_into(into, user, guild):
    """
    Renders the user.
    
    Parameters
    ----------
    into : `list<str>`
        Container to render to.
    user : ``ClientUserBase``
        The user to render.
    guild : `None | Guild`
        Respective guild to pull nick for.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append(user.full_name)
    
    display_name = user.name_at(guild)
    if user.name != display_name:
        into.append(' [*')
        into.append(display_name)
        into.append('*]')
    
    into.append(' (')
    into.append(str(user.id))
    into.append(')')
    
    return into


def render_channel_into(into, channel):
    """
    Renders the channel.
    
    Parameters
    ----------
    into : `list<str>`
        Container to render to.
    channel : ``Channel``
        The channel to render.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append(channel.display_name)

    channel_type = channel.type
    into.append(' [*')
    into.append(channel_type.name)
    into.append(' ~ ')
    into.append(str(channel_type.value))
    into.append('*]')
    
    into.append(' (')
    into.append(str(channel.id))
    into.append(')')
    
    return into


def render_index_into(into, index):
    """
    Renders the given index.
    
    Parameters
    ----------
    into : `list<str>`
        Container to render to.
    index : `int`
        The index to render.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append(repr(index))
    into.append('.: ')
    return into


def render_role_into(into, role):
    """
    Renders the role.
    
    Parameters
    ----------
    into : `list<str>`
        Container to render to.
    role : ``Role``
        The role to render.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append(role.name)
    into.append(' (')
    into.append(repr(role.id))
    into.append(')')
    return into


def iter_render_listing_into(into, elements, limit):
    """
    Iterates over the given `elements` list yielding its elements till `limit` is reached.
    Renders `index` before yielding and renders new line after if applicable.
    If there were any elements truncated renders that at the of the iteration.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    into : `list<str>`
        Container to render to.
    elements : `list`
        Elements to yield from.
    limit : `int`
        The maximal amount of elements before truncate.
    
    Yields
    ------
    element : `object`
    """
    length = len(elements)
    if not length:
        return
    
    if limit >= length:
        truncated = 0
    else:
        truncated = length - limit
        length = limit
    
    index = 0
    
    while True:
        element = elements[index]
        index += 1
        into = render_index_into(into, index)
        
        yield element
        
        if index == length:
            break
        
        into.append('\n')
        continue
    
    if truncated:
        into.append('\n(')
        into.append(str(truncated))
        into.append(' truncated)')


def render_voters_into(into, voters, guild):
    """
    Builds attachment content containing voters.
    
    Parameters
    ----------
    into : `list<str>`
        Container to render to.
    voters : `set<ClientUserBase>`
        Voters to show.
    guild : `None | Guild` = `None`
        The respective guild where the votes were counted at.
    
    Returns
    -------
    into : `list<str>`
    """
    for user in iter_render_listing_into(into, sorted(voters), VOTERS_MAX):
        into = render_user_into(into, user, guild)
    
    return into


def render_nullable_emoji_into(into, emoji):
    """
    Renders the emoji into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    
    emoji : ``None | Emoji``
        The emoji to render.
    
    Returns
    -------
    into : `list<str>`
    """
    if emoji is None:
        into.append('null')
    else:
        into.append(emoji.name)
        into.append(' (')
        into.append(str(emoji.id))
        into.append(')')
    
    return into


def render_nullable_string_tuple_into(into, value):
    """
    Renders a nullable string tuple.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    
    Parameters
    ----------
    value : `None | tuple<str>`
        Value to render.
    
    Returns
    -------
    into : `list<str>`
    """
    if value is None:
        into.append('*none*')
    
    else:
        field_added = False
        
        for element in value:
            if field_added:
                into.append(', ')
            else:
                field_added = True
            
            into.append(repr(element))
    
    return into
