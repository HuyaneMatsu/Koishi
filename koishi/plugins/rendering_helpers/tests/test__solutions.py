from datetime import datetime as DateTime

import vampytest
from hata import GuildProfile, GuildProfileFlag, Role, User, UserFlag

from ..solutions import build_guild_profile_description, build_user_description

from .mocks import DateTimeMock, is_instance_mock


def _iter_options__build_user_description():
    user_0 = User.precreate(
        236597316419584000,
        name = 'koishi',
    )
    
    yield (
        user_0,
        DateTime(2016, 10, 14, 21, 13, 36),
        (
            f'Created: 2016-10-14 21:13:16 [*20 seconds ago*]\n'
            f'Profile: <@{user_0.id}>\n'
            f'ID: {user_0.id}'
        )
    )
    
    user_1 = User.precreate(
        236597320613888000,
        name = 'koishi',
        display_name = 'koi',
        flags = UserFlag().update_by_keys(staff = True),
        
    )
    
    yield (
        user_1,
        DateTime(2016, 10, 14, 21, 13, 46),
        (
            f'Created: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
            f'Profile: <@{user_1.id}>\n'
            f'ID: {user_1.id}\n'
            f'Display name: koi\n'
            f'Flags: staff'
        )
    )


@vampytest._(vampytest.call_from(_iter_options__build_user_description()).returning_last())
def test__build_user_description(user, current_date_time):
    """
    Tests whether ``build_user_description`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to render its description of.
    current_date_time : `DateTime`
        The current time to use as a reference.
    
    Returns
    -------
    output : `str`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        build_user_description, 4, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    return mocked(user)


def _iter_options__build_guild_profile_description():
    # No fields
    yield (
        GuildProfile(),
        DateTime(2016, 10, 14, 21, 13, 36),
        (
            f'Joined: *none*\n'
            f'Roles: *none*'
        )
    )
    
    # Timed out until is in the past
    yield (
        GuildProfile(
            timed_out_until = DateTime(2016, 10, 14, 21, 12, 46),
        ),
        DateTime(2016, 10, 14, 21, 13, 36),
        (
            f'Joined: *none*\n'
            f'Roles: *none*'
        )
    )
    
    # All fields
    role_0 = Role.precreate(202307180000)
    role_1 = Role.precreate(202307180001)
    
    yield (
        GuildProfile(
            joined_at = DateTime(2016, 10, 14, 21, 13, 17),
            role_ids = [role_0.id, role_1.id],
            nick = 'koi',
            flags = GuildProfileFlag().update_by_keys(rejoined = True, onboarding_completed = True),
            boosts_since = DateTime(2016, 10, 14, 21, 13, 18),
            timed_out_until = DateTime(2016, 10, 14, 21, 14, 46),
        ),
        DateTime(2016, 10, 14, 21, 13, 46),
        (
            f'Joined: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
            f'Roles: <@&{role_1.id}>, <@&{role_0.id}>\n'
            f'Nick: koi\n'
            f'Booster since: 2016-10-14 21:13:18 [*28 seconds*]\n'
            f'Timed out until: 2016-10-14 21:14:46 [*1 minute*]\n'
            f'Flags: rejoined, onboarding completed'
        )
    )


@vampytest._(vampytest.call_from(_iter_options__build_guild_profile_description()).returning_last())
def test__build_guild_profile_description(guild_profile, current_date_time):
    """
    Tests whether ``build_guild_profile_description`` works as intended.
    
    Parameters
    ----------
    guild_profile : ``GuildProfile``
        The user's guild profile.
    current_date_time : `DateTime`
        The current time to use as a reference.
    
    Returns
    -------
    output : `str`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        build_guild_profile_description, 4, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    return mocked(guild_profile)
