__all__ = ()

from hata import DATETIME_FORMAT_CODE, elapsed_time


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
        
        if fields_added > 20:
            into.append('... +')
            into.append(str(len(roles) - 20))
            break
        
        into.append(role.mention)
        continue
    
    return into


def render_date_time_into(into, date_time, add_ago):
    """
    Renders the given date time's string value into the given string container. 
    
    Parameters
    ----------
    into : `list` of `str`
        Container.
    date_time : `None`, `DateTime`
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
    into : `list` of `str`
        List to extend.
    flags : ``FlagBase``
        The flags to render.
    
    Returns
    -------
    into : `list` of `str`
    """
    field_added = False
    
    for flag_name in flags:
        if field_added:
            into.append(', ')
        else:
            field_added = True
        
        into.append(flag_name.replace('_', ' '))
    
    return into
