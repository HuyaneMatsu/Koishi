from datetime import datetime as DateTime

import vampytest
from hata import GuildProfile, GuildProfileFlag, Role, User, UserFlag

from ..constants import GUILD_PROFILE_MODE_GENERAL, GUILD_PROFILE_MODE_JOIN, GUILD_PROFILE_MODE_LEAVE
from ..solution_renderers import (
    render_guild_profile_description_into, render_nullable_guild_profile_description_into,
    render_nulled_guild_profile_description_into, render_user_description_into
)

from .mocks import DateTimeMock, is_instance_mock


def _iter_options__render_user_description_into():
    user_0 = User.precreate(
        236597316419584000,
        name = 'koishi',
    )
    
    yield (
        False,
        user_0,
        DateTime(2016, 10, 14, 21, 13, 36),
        (
            (
                f'Created: 2016-10-14 21:13:16 [*20 seconds ago*]\n'
                f'Profile: <@{user_0.id}>\n'
                f'ID: {user_0.id}'
            ),
            True,
        )
    )
    
    # field already added
    yield (
        True,
        user_0,
        DateTime(2016, 10, 14, 21, 13, 36),
        (
            (
                f'\n'
                f'Created: 2016-10-14 21:13:16 [*20 seconds ago*]\n'
                f'Profile: <@{user_0.id}>\n'
                f'ID: {user_0.id}'
            ),
            True,
        )
    )
    
    user_1 = User.precreate(
        236597320613888000,
        name = 'koishi',
        display_name = 'koi',
        flags = UserFlag().update_by_keys(staff = True),
        
    )
    
    yield (
        False,
        user_1,
        DateTime(2016, 10, 14, 21, 13, 46),
        (
            (
                f'Created: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
                f'Profile: <@{user_1.id}>\n'
                f'ID: {user_1.id}\n'
                f'Display name: koi\n'
                f'Flags: staff'
            ),
            True,
        )
    )


@vampytest._(vampytest.call_from(_iter_options__render_user_description_into()).returning_last())
def test__render_user_description_into(field_added, user, current_date_time):
    """
    Tests whether ``render_user_description_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether there were already fields added.
    user : ``ClientUserBase``
        The user to render its description of.
    current_date_time : `DateTime`
        The current time to use as a reference.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        render_user_description_into, 4, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    into, field_added = mocked([], field_added, user)
    return ''.join(into), field_added



def _iter_options__render_guild_profile_description_into():
    # No fields
    yield (
        False,
        GuildProfile(),
        GUILD_PROFILE_MODE_GENERAL,
        DateTime(2016, 10, 14, 21, 13, 36),
        (
            (
                f'Joined: *none*\n'
                f'Roles: *none*'
            ),
            True,
        )
    )
    
    # Field already added
    yield (
        True,
        GuildProfile(),
        GUILD_PROFILE_MODE_GENERAL,
        DateTime(2016, 10, 14, 21, 13, 36),
        (
            (
                f'\n'
                f'Joined: *none*\n'
                f'Roles: *none*'
            ),
            True,
        )
    )
    # Timed out until is in the past
    yield (
        False,
        GuildProfile(
            timed_out_until = DateTime(2016, 10, 14, 21, 12, 46),
        ),
        GUILD_PROFILE_MODE_GENERAL,
        DateTime(2016, 10, 14, 21, 13, 36),
        (
            (
                f'Joined: *none*\n'
                f'Roles: *none*'
            ),
            True,
        )
    )
    
    # All fields
    role_0 = Role.precreate(202307180000)
    role_1 = Role.precreate(202307180001)
    
    yield (
        False,
        GuildProfile(
            joined_at = DateTime(2016, 10, 14, 21, 13, 17),
            role_ids = [role_0.id, role_1.id],
            nick = 'koi',
            flags = GuildProfileFlag().update_by_keys(rejoined = True, onboarding_completed = True),
            boosts_since = DateTime(2016, 10, 14, 21, 13, 18),
            timed_out_until = DateTime(2016, 10, 14, 21, 14, 46),
        ),
        GUILD_PROFILE_MODE_GENERAL,
        DateTime(2016, 10, 14, 21, 13, 46),
        (
            (
                f'Joined: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
                f'Roles: <@&{role_1.id}>, <@&{role_0.id}>\n'
                f'Nick: koi\n'
                f'Booster since: 2016-10-14 21:13:18 [*28 seconds*]\n'
                f'Timed out until: 2016-10-14 21:14:46 [*1 minute*]\n'
                f'Flags: rejoined, onboarding completed'
            ),
            True,
        )
    )

    # Join with roles

    yield (
        False,
        GuildProfile(
            joined_at = DateTime(2016, 10, 14, 21, 13, 17),
            role_ids = [role_0.id, role_1.id],
        ),
        GUILD_PROFILE_MODE_JOIN,
        DateTime(2016, 10, 14, 21, 13, 46),
        (
            (
                f'Joined: 2016-10-14 21:13:17\n'
                f'Roles: <@&{role_1.id}>, <@&{role_0.id}>'
            ),
            True,
        )
    )
    
    # Join without roles
    
    yield (
        False,
        GuildProfile(
            joined_at = DateTime(2016, 10, 14, 21, 13, 17),
            role_ids = None,
        ),
        GUILD_PROFILE_MODE_JOIN,
        DateTime(2016, 10, 14, 21, 13, 46),
        (
            (
                f'Joined: 2016-10-14 21:13:17'
            ),
            True,
        )
    )

    # Leave with roles
    
    yield (
        False,
        GuildProfile(
            joined_at = DateTime(2016, 10, 14, 21, 13, 17),
            role_ids = [role_0.id, role_1.id],
        ),
        GUILD_PROFILE_MODE_LEAVE,
        DateTime(2016, 10, 14, 21, 13, 46),
        (
            (
                f'Joined: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
                f'Roles: <@&{role_1.id}>, <@&{role_0.id}>'
            ),
            True,
        )
    )

    # Leave without roles
    
    yield (
        False,
        GuildProfile(
            joined_at = DateTime(2016, 10, 14, 21, 13, 17),
            role_ids = None
        ),
        GUILD_PROFILE_MODE_LEAVE,
        DateTime(2016, 10, 14, 21, 13, 46),
        (
            (
                f'Joined: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
                f'Roles: *none*'
            ),
            True,
        )
    )


@vampytest._(vampytest.call_from(_iter_options__render_guild_profile_description_into()).returning_last())
def test__render_guild_profile_description_into(field_added, guild_profile, mode, current_date_time):
    """
    Tests whether ``render_guild_profile_description_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether there were fields added already.
    guild_profile : ``GuildProfile``
        The user's guild profile.
    mode : `int`
        Rendering mode.
    current_date_time : `DateTime`
        The current time to use as a reference.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        render_guild_profile_description_into, 4, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    into, field_added = mocked([], field_added, guild_profile, mode)
    return ''.join(into), field_added


def _iter_options__render_nulled_guild_profile_description_into():
    current_date = DateTime(2016, 10, 14, 21, 13, 36)
    
    # General
    yield (
        False,
        GUILD_PROFILE_MODE_GENERAL,
        current_date,
        (
            (
                'Joined: *none*'
                '\nRoles: *none*'
            ),
            True,
        ),
    )

    yield (
        True,
        GUILD_PROFILE_MODE_GENERAL,
        current_date,
        (
            (
                '\nJoined: *none*'
                '\nRoles: *none*'
            ),
            True,
        ),
    )
    
    # Join
    yield (
        False,
        GUILD_PROFILE_MODE_JOIN,
        current_date,
        (
            (
                'Joined: 2016-10-14 21:13:36'
            ),
            True,
        ),
    )

    yield (
        True,
        GUILD_PROFILE_MODE_JOIN,
        current_date,
        (
            (
                '\nJoined: 2016-10-14 21:13:36'
            ),
            True,
        ),
    )
    
    # Leave
    
    yield (
        False,
        GUILD_PROFILE_MODE_LEAVE,
        current_date,
        (
            (
                'Joined: *none*'
                '\nRoles: *none*'
            ),
            True,
        ),
    )

    yield (
        True,
        GUILD_PROFILE_MODE_LEAVE,
        current_date,
        (
            (
                '\nJoined: *none*'
                '\nRoles: *none*'
            ),
            True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__render_nulled_guild_profile_description_into()).returning_last())
def test__render_nulled_guild_profile_description_into(field_added, mode, current_date_time):
    """
    Tests whether ``render_nulled_guild_profile_description_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether there were fields added already.
    mode : `int`
        Rendering mode.
    current_date_time : `DateTime`
        The current time to use as a reference.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        render_nulled_guild_profile_description_into, 0, {'DateTime': DateTimeMock}
    )
    
    into, field_added = mocked([], field_added, mode)
    return ''.join(into), field_added


def _iter_options__render_nullable_guild_profile_description_into():
    current_date = DateTime(2016, 10, 14, 21, 13, 36)
    
    yield (
        False,
        None,
        GUILD_PROFILE_MODE_LEAVE,
        current_date,
        (
            (
                'Joined: *none*'
                '\nRoles: *none*'
            ),
            True,
        ),
    )
    
    yield (
        False,
        GuildProfile(
            joined_at = DateTime(2016, 10, 14, 21, 13, 7)
        ),
        GUILD_PROFILE_MODE_LEAVE,
        current_date,
        (
            (
                f'Joined: 2016-10-14 21:13:07 [*29 seconds ago*]\n'
                f'Roles: *none*'
            ),
            True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__render_nullable_guild_profile_description_into()).returning_last())
def test__render_nullable_guild_profile_description_into(field_added, guild_profile, mode, current_date_time):
    """
    Tests whether ``render_nullable_guild_profile_description_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether there were fields added already.
    guild_profile : `None`, ``GuildProfile``
        The user's guild profile.
    mode : `int`
        Rendering mode.
    current_date_time : `DateTime`
        The current time to use as a reference.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        render_nullable_guild_profile_description_into, 5, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    into, field_added = mocked([], field_added, guild_profile, mode)
    return ''.join(into), field_added
