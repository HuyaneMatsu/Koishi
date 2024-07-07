__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import DATETIME_FORMAT_CODE, elapsed_time

from .constants import DATE_TIME_CONDITION_ALL, DATE_TIME_CONDITION_PAST, DATE_TIME_CONDITION_FUTURE
from .value_renderers import (
    render_channel_into, render_role_mentions_into, render_date_time_with_relative_into, render_flags_into,
    render_user_into
)


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
    into, field_added, date_time, *, add_ago = True, optional = True, title = 'Date', condition = DATE_TIME_CONDITION_ALL
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
        date_time_nulled = date_time <= DateTime.now(TimeZone.utc)
    elif condition == DATE_TIME_CONDITION_PAST:
        date_time_nulled = date_time >= DateTime.now(TimeZone.utc)
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


def render_preinstanced_field_into(into, field_added, preinstanced, *, optional = True, title = 'Type'):
    """
    Renders a preinstanced field into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    preinstanced : ``PreinstancedBase``
        The preinstanced value to render.
    optional : `bool` = `True`, Optional (Keyword only)
        Whether should not render if `preinstanced` is empty.
    title : `str` = `'Type'`, Optional (Keyword only)
        The title of the line.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if (not optional) or preinstanced.value:
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append(title)
        into.append(': ')
        into.append(preinstanced.name)
        into.append(' ~ ')
        into.append(str(preinstanced.value))
    
    return into, field_added


def render_user_field_into(into, field_added, user, *, guild = None, optional = True, title = 'User'):
    """
    Renders a preinstanced field into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    user : `None | ClientUserBase`
        The user to render.
    guild : `None | Guild` = `None`, Optional (Keyword only)
        The guild to pull the user's nick name for.
    optional : `bool` = `True`, Optional (Keyword only)
        Whether should not render if `user` is `None`.
    title : `str` = `'User'`, Optional (Keyword only)
        The title of the line.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if (not optional) or (user is not None):
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append(title)
        into.append(': ')
        
        if user is None:
            into.append('*none*')
        else:
            into = render_user_into(into, user, guild)
    
    return into, field_added


def render_channel_field_into(into, field_added, channel, *, optional = True, title = 'Channel'):
    """
    Renders a preinstanced field into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    channel : `None | Channel`
        The channel to render.
    optional : `bool` = `True`, Optional (Keyword only)
        Whether should not render if `channel` is `None`.
    title : `str` = `'Channel'`, Optional (Keyword only)
        The title of the line.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if (not optional) or (channel is not None):
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append(title)
        into.append(': ')
        
        if channel is None:
            into.append('*none*')
        else:
            into = render_channel_into(into, channel)
    
    return into, field_added


def render_attachments_field_into(into, field_added, attachments, *, optional = True, title = 'Attachments'):
    """
    Renders a preinstanced field into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    attachments : `None | set<Attachment>`
        The attachments to render.
    optional : `bool` = `True`, Optional (Keyword only)
        Whether should not render if `attachments` is `None`.
    title : `str` = `'Attachment'`, Optional (Keyword only)
        The title of the line.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if (not optional) or (attachments is not None):
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append(title)
        into.append(':')
        
        if attachments is None:
            into.append(' *none*')
        
        else:
            for attachment in attachments:
                url = attachment.url
                end_index = url.find('?')
                if end_index != -1:
                    url = url[:end_index]
                
                into.append('\n- [')
                into.append(attachment.name)
                into.append('](')
                into.append(url)
                into.append(')')
    
    return into, field_added
