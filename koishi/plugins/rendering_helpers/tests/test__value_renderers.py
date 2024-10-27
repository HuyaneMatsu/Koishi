from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Channel, ChannelType, Emoji, Role, UserFlag

from ..constants import ROLE_MENTIONS_MAX
from ..value_renderers import (
    render_channel_into, render_date_time_with_relative_into, render_flags_into, render_nullable_emoji_into,
    render_nullable_string_tuple_into, render_role_mentions_into
)

from .mocks import DateTimeMock, is_instance_mock


def _iter_options__render_role_mentions_into():
    role_0 = Role.precreate(202307170000)
    role_1 = Role.precreate(202307170001)
    
    yield (role_0,), f'{role_0:m}'
    yield (role_0, role_1), f'{role_1:m}, {role_0:m}'
    yield (
        (*(role_0 for counter in range(30)),),
        (role_0.mention + ', ') * ROLE_MENTIONS_MAX + f'... +{30 - ROLE_MENTIONS_MAX}'
    )


@vampytest._(vampytest.call_from(_iter_options__render_role_mentions_into()).returning_last())
def test__render_role_mentions_into(input_roles):
    """
    Tests whether ``render_role_mentions_into`` works as intended.
    
    Parameters
    ----------
    input_roles : `None | tuple<Role>`
        Roles to render.
    
    Returns
    -------
    output : `str`
    """
    into = render_role_mentions_into([], input_roles)
    return ''.join(into)


def _iter_options__render_date_time_with_relative_into():
    yield (
        DateTime(2016, 10, 14, 21, 13, 16, tzinfo = TimeZone.utc),
        DateTime(2016, 10, 14, 21, 13, 26, tzinfo = TimeZone.utc),
        True,
        '2016-10-14 21:13:16 [*10 seconds ago*]',
    )
    
    yield (
        DateTime(2016, 10, 14, 21, 13, 16, tzinfo = TimeZone.utc),
        DateTime(2016, 10, 14, 21, 13, 26, tzinfo = TimeZone.utc),
        False,
        '2016-10-14 21:13:16 [*10 seconds*]',
    )


@vampytest._(vampytest.call_from(_iter_options__render_date_time_with_relative_into()).returning_last())
def test__render_date_time_with_relative_into(input_date_time, current_date_time, add_ago):
    """
    Tests whether ``render_date_time_with_relative_into`` works as intended.
    
    Parameters
    ----------
    input_date_time : `DateTime`
        Input datetime to render.
    current_date_time : `DateTime`
        The current date time. Used for mocking.
    add_ago : `bool`
        Whether `ago` should be added into the representation.
    
    Returns
    -------
    output : `str`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        render_date_time_with_relative_into, 3, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    into = mocked([], input_date_time, add_ago)
    return ''.join(into)


def _iter_options__render_flags_into():
    yield UserFlag(), '*none*'
    yield UserFlag().update_by_keys(staff = True), 'staff'
    yield UserFlag().update_by_keys(staff = True, team_user = True), 'staff, team user'


@vampytest._(vampytest.call_from(_iter_options__render_flags_into()).returning_last())
def test__render_flags_into(input_flags):
    """
    Tests whether ``render_flags_into`` works as intended.
    
    Parameters
    ----------
    input_flags : ``FLagBase``
        Flags to render.
    
    Returns
    -------
    output : `str`
    """
    into = render_flags_into([], input_flags)
    return ''.join(into)


def _iter_options__render_nullable_emoji_into():
    emoji = Emoji.precreate(202410150010, name = 'keine')
    
    yield (
        None,
        'null',
    )
    
    yield (
        emoji,
        f'{emoji.name} ({emoji.id!s})',
    )


@vampytest._(vampytest.call_from(_iter_options__render_nullable_emoji_into()).returning_last())
def test__render_nullable_emoji_into(input_value):
    """
    Tests whether ``render_nullable_emoji_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | Emoji`
        The value to render.
    
    Returns
    -------
    output : `str`
    """
    into = render_nullable_emoji_into([], input_value)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)


def _iter_options__render_channel_into():
    channel = Channel.precreate(202410150019, channel_type = ChannelType.guild_text, name = 'keine')
    
    yield (
        channel,
        f'{channel.name} [*{channel.type.name!s} ~ {channel.type.value!s}*] ({channel.id!s})',
    )


@vampytest._(vampytest.call_from(_iter_options__render_channel_into()).returning_last())
def test__render_channel_into(input_value):
    """
    Tests whether ``render_channel_into`` works as intended.
    
    Parameters
    ----------
    input_value : ``Channel``
        The value to render.
    
    Returns
    -------
    output : `str`
    """
    into = render_channel_into([], input_value)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)


def _iter_options__render_nullable_string_tuple_into():
    yield (
        None,
        '*none*',
    )
    
    yield (
        ('hey',),
        f'\'hey\'',
    )
    
    yield (
        ('hey', 'mister'),
        f'\'hey\', \'mister\'',
    )


@vampytest._(vampytest.call_from(_iter_options__render_nullable_string_tuple_into()).returning_last())
def test__render_nullable_string_tuple_into(input_value):
    """
    Tests whether ``render_nullable_string_tuple_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<str>`
        The value to render.
    
    Returns
    -------
    output : `str`
    """
    into = render_nullable_string_tuple_into([], input_value)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
