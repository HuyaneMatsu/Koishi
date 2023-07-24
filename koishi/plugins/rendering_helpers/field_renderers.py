__all__ = ()

from datetime import datetime as DateTime

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import DATETIME_FORMAT_CODE, elapsed_time

from .constants import DATE_TIME_CONDITION_ALL, DATE_TIME_CONDITION_PAST, DATE_TIME_CONDITION_FUTURE
from .value_renderers import render_role_mentions_into, render_date_time_with_relative_into, render_flags_into


def render_role_mentions_field_into(into, field_added, roles, *, optional = True, title = 'Roles'):
    """
    Renders roles field into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    roles : `None`, `tuple` of ``Role``
        The roles to render.
    optional : `bool` = `True`, Optional (Keyword only)
        Whether should not render if `roles` is `None`.
    title : `str` = `'Roles'`, Optional (Keyword only)
        The title of the field.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if (not optional) or (roles is not None):
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append(title)
        into.append(': ')
        if roles is None:
            into.append('*none*')
        else:
            into = render_role_mentions_into(into, roles)
    
    return into, field_added


def render_date_time_with_relative_field_into(
    into, field_added, date_time, *, add_ago = True, optional = True, title = 'Date', condition = 0
):
    """
    Renders date time field with relative representation into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    date_time : `None`, `DateTime`
        The date time to render.
    add_ago : `bool` = `True`, Optional (Keyword only)
        Whether `ago` word should be added into the relative date option.
    optional : `bool` = `True`, Optional (Keyword only)
        Whether should not render if `date_time` is `None`.
    title : `str` = `'Date'`, Optional (Keyword only)
        The title of the line.
    condition : `int` = `DATE_TIME_CONDITION_ALL`, Optional (Keyword only)
        Additional condition to check before rendering.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if date_time is None:
        date_time_nulled = True
    elif condition == DATE_TIME_CONDITION_ALL:
        date_time_nulled = False
    elif condition == DATE_TIME_CONDITION_FUTURE:
        date_time_nulled = date_time <= DateTime.utcnow()
    elif condition == DATE_TIME_CONDITION_PAST:
        date_time_nulled = date_time >= DateTime.utcnow()
    else:
        date_time_nulled = False
    
    if (not optional) or (not date_time_nulled):
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append(title)
        into.append(': ')
        if date_time_nulled:
            into.append('*none*')
        else:
            into = render_date_time_with_relative_into(into, date_time, add_ago)
        
    return into, field_added


def render_date_time_field_into(into, field_added, date_time, *, optional = True, title = 'Date'):
    """
    Renders date time field into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    date_time : `None`, `DateTime`
        The date time to render.
    add_ago : `bool` = `True`, Optional (Keyword only)
        Whether `ago` word should be added into the relative date option.
    optional : `bool` = `True`, Optional (Keyword only)
        Whether should not render if `date_time` is `None`.
    title : `str` = `'Date'`, Optional (Keyword only)
        The title of the line.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if (not optional) or (date_time is not None):
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append(title)
        into.append(': ')
        if (date_time is None):
            into.append('*none*')
        else:
            into.append(format(date_time, DATETIME_FORMAT_CODE))
    
    return into, field_added


def render_date_time_difference_field_into(
    into, field_added, date_time_0, date_time_1, *, optional = True, title = 'Date'
):
    """
    Renders date difference into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    date_time_0 : `None`, `DateTime`
        Date to make the difference from.
    date_time_1 : `None`, `DateTime`
        The other date.
    optional : `bool` = `True`, Optional (Keyword only)
        Whether should not render if `date_time` is `None`.
    title : `str` = `'Date'`, Optional (Keyword only)
        The title of the line.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if (not optional) or (date_time_0 is not None) and (date_time_1 is not None):
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append(title)
        into.append(' difference: ')
        
        if (date_time_0 is None) or (date_time_1 is None):
            difference_string = 'N/A'
        else:
            difference_string = elapsed_time(RelativeDelta(date_time_0, date_time_1))
        into.append(difference_string)
    
    return into, field_added


def render_flags_field_into(into, field_added, flags, *, optional = True, title = 'Flags'):
    """
    Renders flags field into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    flags : ``FlagBase``
        The flags to render.
    optional : `bool` = `True`, Optional (Keyword only)
        Whether should not render if `flags` is empty.
    title : `str` = `'Flags'`, Optional (Keyword only)
        The title of the line.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if (not optional) or flags:
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append(title)
        into.append(': ')
        if flags:
            into = render_flags_into(into, flags)
        else:
            into.append('*none*')
        
    return into, field_added


def render_string_field_into(into, field_added, string, *, optional = True, title = 'Value'):
    """
    Renders string field into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    string : `None`, `str`
        The string to render.
    optional : `bool` = `True`, Optional (Keyword only)
        Whether should not render if `flags` is empty.
    title : `str` = `'Flags'`, Optional (Keyword only)
        The title of the line.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if (not optional) or (string is not None):
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append(title)
        into.append(': ')
        if string is None:
            into.append('*none*')
        else:
            into.append(string)
        
    return into, field_added
