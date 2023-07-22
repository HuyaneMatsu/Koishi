from datetime import datetime as DateTime

import vampytest
from hata import Role, UserFlag

from ..field_renderers import (
    render_date_time_field_into, render_flags_field_into, render_role_mentions_field_into, render_string_field_into
)

from .mocks import DateTimeMock, is_instance_mock


def _iter_options__render_role_mentions_field_into():
    role_0 = Role.precreate(202307190000)
    role_1 = Role.precreate(202307190001)
    
    n_roles = (*(role_0 for counter in range(30)),)
    n_roles_repr = (role_0.mention + ', ') * 20 + '... +10'
    
    yield False, None, False, 'Roles', ('Roles: *none*', True)
    yield True, None, False, 'Roles', ('\nRoles: *none*', True)
    yield False, (role_0,), False, 'Roles', (f'Roles: {role_0:m}', True)
    yield True, (role_0,), False, 'Roles', (f'\nRoles: {role_0:m}', True)
    yield False, (role_0, role_1), False, 'Roles', (f'Roles: {role_1:m}, {role_0:m}', True)
    yield True, (role_0, role_1), False, 'Roles', (f'\nRoles: {role_1:m}, {role_0:m}', True)
    yield False, n_roles, False, 'Roles', (f'Roles: {n_roles_repr}', True)
    yield True, n_roles, False, 'Roles', (f'\nRoles: {n_roles_repr}', True)

    yield False, None, True, 'Roles', ('', False)
    yield True, None, True, 'Roles', ('', True)
    yield False, (role_0,), True, 'Roles', (f'Roles: {role_0:m}', True)
    yield True, (role_0,), True, 'Roles', (f'\nRoles: {role_0:m}', True)
    yield False, (role_0, role_1), True, 'Roles', (f'Roles: {role_1:m}, {role_0:m}', True)
    yield True, (role_0, role_1), True, 'Roles', (f'\nRoles: {role_1:m}, {role_0:m}', True)
    yield False, n_roles, True, 'Roles', (f'Roles: {n_roles_repr}', True)
    yield True, n_roles, True, 'Roles', (f'\nRoles: {n_roles_repr}', True)

    # Just 1 version should be enough
    yield False, (role_0,), True, 'Confusion', (f'Confusion: {role_0:m}', True)


@vampytest._(vampytest.call_from(_iter_options__render_role_mentions_field_into()).returning_last())
def test__render_role_mentions_field_into(field_added, roles, optional, title):
    """
    Tests whether ``render_role_mentions_field_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether any fields were added already.
    roles : `None`, `tuple` of ``Role``
        The roles to render.
    optional : `bool`
        Whether should not render if `roles` is `None`.
    title : `str`
        The title of the field.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    into, field_added = render_role_mentions_field_into([], field_added, roles, optional = optional, title = title)
    return ''.join(into), field_added


def _iter_options__render_date_time_field_into():
    date_time = DateTime(2016, 10, 14, 21, 13, 16)
    current = DateTime(2016, 10, 14, 21, 13, 26)
    
    yield current, False, None, False, False, 'Date', ('Date: *none*', True)
    yield current, True, None, False, False, 'Date', ('\nDate: *none*', True)
    yield current, False, date_time, False, False, 'Date', ('Date: 2016-10-14 21:13:16 [*10 seconds*]', True)
    yield current, True, date_time, False, False, 'Date', ('\nDate: 2016-10-14 21:13:16 [*10 seconds*]', True)
    yield current, False, None, True, False, 'Date', ('Date: *none*', True)
    yield current, True, None, True, False, 'Date', ('\nDate: *none*', True)
    yield current, False, date_time, True, False, 'Date', ('Date: 2016-10-14 21:13:16 [*10 seconds ago*]', True)
    yield current, True, date_time, True, False, 'Date', ('\nDate: 2016-10-14 21:13:16 [*10 seconds ago*]', True)
    yield current, False, None, False, True, 'Date', ('', False)
    yield current, True, None, False, True, 'Date', ('', True)
    yield current, False, date_time, False, True, 'Date', ('Date: 2016-10-14 21:13:16 [*10 seconds*]', True)
    yield current, True, date_time, False, True, 'Date', ('\nDate: 2016-10-14 21:13:16 [*10 seconds*]', True)
    yield current, False, None, True, True, 'Date', ('', False)
    yield current, True, None, True, True, 'Date', ('', True)
    yield current, False, date_time, True, True, 'Date', ('Date: 2016-10-14 21:13:16 [*10 seconds ago*]', True)
    yield current, True, date_time, True, True, 'Date', ('\nDate: 2016-10-14 21:13:16 [*10 seconds ago*]', True)
    
    # 1 should be enough
    yield current, False, date_time, False, True, 'Created at', ('Created at: 2016-10-14 21:13:16 [*10 seconds*]', True)


@vampytest._(vampytest.call_from(_iter_options__render_date_time_field_into()).returning_last())
def test__render_date_time_field_into(current_date, field_added, date_time, add_ago, optional, title):
    """
    Tests whether ``render_role_mentions_field_into`` works as intended.
    
    Parameters
    ----------
    current_date : `DateTime`
        The current time to use as a reference.
    field_added : `bool`
        Whether any fields were added already.
    date_time : `None`, `DateTime`
        The date to render.
    add_ago : `bool`
        Whether `ago` word should be added into the relative date option.
    optional : `bool`
        Whether should not render if `date_time` is `None`.
    title : `str`
        The title of the field.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    DateTimeMock.set_current(current_date)
    mocked = vampytest.mock_globals(
        render_date_time_field_into, 3, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    into, field_added = mocked(
        [], field_added, date_time, add_ago = add_ago, optional = optional, title = title
    )
    return ''.join(into), field_added




def _iter_options__render_date_time_field_into():
    current = DateTime(2016, 10, 14, 21, 13, 26)
    
    yield current, None, -1, ('', False)
    yield current, None, 0, ('', False)
    yield current, None, 1, ('', False)
    
    yield current, DateTime(2016, 10, 14, 21, 13, 36), -1, ('', False)
    yield current, DateTime(2016, 10, 14, 21, 13, 36), 0, ('Date: 2016-10-14 21:13:36 [*10 seconds*]', True)
    yield current, DateTime(2016, 10, 14, 21, 13, 36), 1, ('Date: 2016-10-14 21:13:36 [*10 seconds*]', True)
    
    yield current, DateTime(2016, 10, 14, 21, 13, 16), -1, ('Date: 2016-10-14 21:13:16 [*10 seconds*]', True)
    yield current, DateTime(2016, 10, 14, 21, 13, 16), 0, ('Date: 2016-10-14 21:13:16 [*10 seconds*]', True)
    yield current, DateTime(2016, 10, 14, 21, 13, 16), 1,  ('', False)


@vampytest._(vampytest.call_from(_iter_options__render_date_time_field_into()).returning_last())
def test__render_date_time_field_into__when(current_date, date_time, when):
    """
    Tests whether ``render_role_mentions_field_into`` works as intended.
    
    Case: `when` is defined.
    
    Parameters
    ----------
    current_date : `DateTime`
        The current time to use as a reference.
    date_time : `None`, `DateTime`
        The date to render.
    when : `int`
        Whether we only wanna render future time, current or perhaps both?
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    DateTimeMock.set_current(current_date)
    mocked = vampytest.mock_globals(
        render_date_time_field_into, 3, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    into, field_added = mocked(
        [], False, date_time, add_ago = False, when = when
    )
    return ''.join(into), field_added


def _iter_options__render_flags_field_into():
    flags_0 = UserFlag()
    flags_0_repr = '*none*'
    flags_1 = UserFlag().update_by_keys(staff = True)
    flags_1_repr = 'staff'
    flags_2 = UserFlag().update_by_keys(staff = True, team_user = True)
    flags_2_repr = 'staff, team user'
    
    yield False, flags_0, False, 'Flags', (f'Flags: {flags_0_repr}', True)
    yield True, flags_0, False, 'Flags', (f'\nFlags: {flags_0_repr}', True)
    yield False, flags_1, False, 'Flags', (f'Flags: {flags_1_repr}', True)
    yield True, flags_1, False, 'Flags', (f'\nFlags: {flags_1_repr}', True)
    yield False, flags_2, False, 'Flags', (f'Flags: {flags_2_repr}', True)
    yield True, flags_2, False, 'Flags', (f'\nFlags: {flags_2_repr}', True)
    yield False, flags_0, True, 'Flags', (f'', False)
    yield True, flags_0, True, 'Flags', (f'', True)
    yield False, flags_1, True, 'Flags', (f'Flags: {flags_1_repr}', True)
    yield True, flags_1, True, 'Flags', (f'\nFlags: {flags_1_repr}', True)
    yield False, flags_2, True, 'Flags', (f'Flags: {flags_2_repr}', True)
    yield True, flags_2, True, 'Flags', (f'\nFlags: {flags_2_repr}', True)
    
    # 1 should be enough
    yield False, flags_1, False, 'User flags', (f'User flags: {flags_1_repr}', True)


@vampytest._(vampytest.call_from(_iter_options__render_flags_field_into()).returning_last())
def test__render_flags_field_into(field_added, flags, optional, title):
    """
    Tests whether ``render_flags_field_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether any fields were added already.
    flags : ``FlagBase``
        The flags to render.
    optional : `bool`
        Whether should not render if `flags` is empty.
    title : `str`
        The title of the line.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    into, field_added = render_flags_field_into([], field_added, flags, optional = optional, title = title)
    return ''.join(into), field_added


def _iter_options__render_string_field_into():
    string_0 = None
    string_0_repr = '*none*'
    string_1 = 'koishi'
    string_1_repr = 'koishi'
    
    yield False, string_0, False, 'Value', (f'Value: {string_0_repr}', True)
    yield True, string_0, False, 'Value', (f'\nValue: {string_0_repr}', True)
    yield False, string_1, False, 'Value', (f'Value: {string_1_repr}', True)
    yield True, string_1, False, 'Value', (f'\nValue: {string_1_repr}', True)
    yield False, string_0, True, 'Value', (f'', False)
    yield True, string_0, True, 'Value', (f'', True)
    yield False, string_1, True, 'Value', (f'Value: {string_1_repr}', True)
    yield True, string_1, True, 'Value', (f'\nValue: {string_1_repr}', True)
    
    # 1 should be enough
    yield False, string_1, False, 'Name', (f'Name: {string_1_repr}', True)


@vampytest._(vampytest.call_from(_iter_options__render_string_field_into()).returning_last())
def test__render_string_field_into(field_added, string, optional, title):
    """
    Tests whether ``render_string_field_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether any fields were added already.
    string : `None`, `str`
        The string to render.
    optional : `bool`
        Whether should not render if `string` is empty.
    title : `str`
        The title of the line.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    into, field_added = render_string_field_into([], field_added, string, optional = optional, title = title)
    return ''.join(into), field_added
