from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import (
    Activity, ActivityAssets, ActivityFlag, ActivityParty, ActivitySecrets, ActivityTimestamps, ActivityType,
    GuildProfile, GuildProfileFlag, Role, User, UserFlag, Status, StatusByPlatform
)

from ..solution_builders import (
    build_activity_description, build_guild_profile_description, build_user_description,
    build_user_join_or_leave_description, build_user_status_description, build_user_with_guild_profile_description
)

from .mocks import DateTimeMock, is_instance_mock


def _iter_options__build_user_description():
    user_0 = User.precreate(
        236597316419584000,
        name = 'koishi',
    )
    
    yield (
        user_0,
        DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc),
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
        DateTime(2016, 10, 14, 21, 13, 46, tzinfo = TimeZone.utc),
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
        build_user_description, 5, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    return mocked(user)


def _iter_options__build_guild_profile_description():
    # No fields
    yield (
        GuildProfile(),
        DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc),
        (
            f'Joined: *none*\n'
            f'Roles: *none*'
        )
    )
    
    # Timed out until is in the past
    yield (
        GuildProfile(
            timed_out_until = DateTime(2016, 10, 14, 21, 12, 46, tzinfo = TimeZone.utc),
        ),
        DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc),
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
            joined_at = DateTime(2016, 10, 14, 21, 13, 17, tzinfo = TimeZone.utc),
            role_ids = [role_0.id, role_1.id],
            nick = 'koi',
            flags = GuildProfileFlag().update_by_keys(rejoined = True, onboarding_completed = True),
            boosts_since = DateTime(2016, 10, 14, 21, 13, 18, tzinfo = TimeZone.utc),
            timed_out_until = DateTime(2016, 10, 14, 21, 14, 46, tzinfo = TimeZone.utc),
        ),
        DateTime(2016, 10, 14, 21, 13, 46, tzinfo = TimeZone.utc),
        (
            f'Joined: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
            f'Roles: <@&{role_1.id}>, <@&{role_0.id}>\n'
            f'Nick: koi\n'
            f'Booster since: 2016-10-14 21:13:18 [*28 seconds*]\n'
            f'Timed out until: 2016-10-14 21:14:46 [*1 minute*]\n'
            f'Flags: onboarding completed, rejoined'
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
        build_guild_profile_description, 5, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    return mocked(guild_profile)


def _iter_options__test__build_user_join_or_leave_description():
    user_0 = User.precreate(
        236597320613888001,
        name = 'koishi',
    )
    
    user_1 = User.precreate(
        236597320613888002,
        name = 'koishi',
        display_name = 'koi',
        flags = UserFlag().update_by_keys(staff = True),
    )
    
    current_date = DateTime(2016, 10, 14, 21, 13, 46, tzinfo = TimeZone.utc)
    
    role_0 = Role.precreate(202307240000)
    role_1 = Role.precreate(202307240001)
    
    guild_profile = GuildProfile(
        joined_at = DateTime(2016, 10, 14, 21, 13, 27, tzinfo = TimeZone.utc),
        role_ids = [role_0.id, role_1.id],
        nick = 'koi',
        flags = GuildProfileFlag().update_by_keys(rejoined = True, onboarding_completed = True),
        boosts_since = DateTime(2016, 10, 14, 21, 13, 18, tzinfo = TimeZone.utc),
        timed_out_until = DateTime(2016, 10, 14, 21, 14, 46, tzinfo = TimeZone.utc),
    )
    
    # Join no fields
    
    yield (
        user_0,
        None,
        True,
        current_date,
        (
            f'Created: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
            f'Profile: <@{user_0.id}>\n'
            f'ID: {user_0.id}\n'
            f'\n'
            f'Joined: 2016-10-14 21:13:46'
        ),
    )
    
    # Leave no fields
    
    yield (
        user_0,
        None,
        False,
        current_date,
        (
            f'Created: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
            f'Profile: <@{user_0.id}>\n'
            f'ID: {user_0.id}\n'
            f'\n'
            f'Joined: *none*\n'
            f'Roles: *none*\n'
            f'\n'
            f'Left: 2016-10-14 21:13:46\n'
            f'Created - joined difference: N/A'
        ),
    )

    # Join all fields
    
    yield (
        user_1,
        guild_profile,
        True,
        current_date,
        (
            f'Created: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
            f'Profile: <@{user_1.id}>\n'
            f'ID: {user_1.id}\n'
            f'Display name: koi\n'
            f'Flags: staff\n'
            f'\n'
            f'Joined: 2016-10-14 21:13:27\n'
            f'Roles: <@&202307240001>, <@&202307240000>\n'
            f'Nick: koi\n'
            f'Booster since: 2016-10-14 21:13:18 [*28 seconds*]\n'
            f'Timed out until: 2016-10-14 21:14:46 [*1 minute*]\n'
            f'Flags: onboarding completed, rejoined'
        ),
    )
    
    # Leave all fields
    
    yield (
        user_1,
        guild_profile,
        False,
        current_date,
        (
            f'Created: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
            f'Profile: <@{user_1.id}>\n'
            f'ID: {user_1.id}\n'
            f'Display name: koi\n'
            f'Flags: staff\n'
            f'\n'
            f'Joined: 2016-10-14 21:13:27 [*19 seconds ago*]\n'
            f'Roles: <@&202307240001>, <@&202307240000>\n'
            f'Nick: koi\n'
            f'Booster since: 2016-10-14 21:13:18 [*28 seconds*]\n'
            f'Timed out until: 2016-10-14 21:14:46 [*1 minute*]\n'
            f'Flags: onboarding completed, rejoined\n'
            f'\n'
            f'Left: 2016-10-14 21:13:46\n'
            f'Created - joined difference: 10 seconds'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__test__build_user_join_or_leave_description()).returning_last())
def test__build_user_join_or_leave_description(user, guild_profile, join, current_date_time):
    """
    Tests whether ``build_user_join_or_leave_description`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who joined or left.
    guild_profile : `None`, ``GuildProfile``
        The user's guild profile.
    join : `bool`
        Whether the user joined or left.
    current_date_time : `DateTime`
        The current time to use as a reference.
    
    Returns
    -------
    description : `str`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        build_user_join_or_leave_description, 6, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    return mocked(user, guild_profile, join)


def _iter_options__build_activity_description():
    current_date = DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc)
    
    # Maximal
    yield (
        Activity(
            name = 'with Kokoro',
            activity_type = ActivityType.spotify,
            activity_id = 202308080000,
            application_id = 202308080001,
            assets = ActivityAssets(
                image_large = 'spotify:Yuuka',
                image_small = 'Yukari',
                text_large = 'Yuyuko',
                text_small = 'Youmu',
            ),
            created_at = DateTime(2016, 10, 14, 21, 13, 26, tzinfo = TimeZone.utc),
            details = 'Satori',
            flags = ActivityFlag().update_by_keys(play = True, embedded = True),
            party = ActivityParty(
                party_id = 'Suika',
                size = 6,
                max_ = 9,
            ),
            secrets = ActivitySecrets(
                join = 'Hecatia',
                match = 'Junko',
                spectate = 'Chiruno',
            ),
            session_id = 'Orin',
            state = 'Okuu',
            sync_id = 'Mr. spider',
            timestamps = ActivityTimestamps(
                end = DateTime(2016, 10, 14, 21, 13, 46, tzinfo = TimeZone.utc),
                start = DateTime(2016, 10, 14, 21, 13, 16, tzinfo = TimeZone.utc),
            ),
            url = 'https://orindance.party/',
        ),
        current_date,
        (
            f'Type: spotify ~ 2\n'
            f'Name: with Kokoro\n'
            f'Timestamp start: 2016-10-14 21:13:16\n'
            f'Timestamp end: 2016-10-14 21:13:46\n'
            f'Details: Satori\n'
            f'State: Okuu\n'
            f'Party id: Suika\n'
            f'Party size: 6\n'
            f'Party max: 9\n'
            f'Assets image large: spotify:Yuuka\n'
            f'Assets text large: Yuyuko\n'
            f'Assets image small: Yukari\n'
            f'Assets text small: Youmu\n'
            f'Secrets join: Hecatia\n'
            f'Secrets match: Junko\n'
            f'Secrets spectate: Chiruno\n'
            f'Spotify album cover url: https://i.scdn.co/image/Yuuka\n'
            f'Url: https://orindance.party/\n'
            f'Sync id: Mr. spider\n'
            f'Session id: Orin\n'
            f'Flags: embedded, play\n'
            f'Application id: 202308080001\n'
            f'Id: 202308080000\n'
            f'Created at: 2016-10-14 21:13:26 [*10 seconds ago*]'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__build_activity_description()).returning_last())
def test__build_activity_description(activity, current_date):
    """
    Tests whether ``build_activity_description`` works as intended.
    
    Parameters
    ----------
    activity : ``Activity``
        The activity to render.
    current_date_time : `DateTime`
        The current time to use as a reference.
    
    Returns
    -------
    description : `str`
    """
    DateTimeMock.set_current(current_date)
    mocked = vampytest.mock_globals(
        build_activity_description, 5, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    return mocked(activity)


def _iter_options__build_user_status_description():
    user_0 = User()
    user_0.status = Status.idle
    user_0.status_by_platform = StatusByPlatform(
        desktop = Status.dnd,
        mobile = Status.idle,
        web = Status.online,
    )
    
    # Maximal
    yield (
        user_0,
        (
            f'Status: idle\n'
            f'- Desktop: dnd\n'
            f'- Mobile: idle\n'
            f'- Web: online'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__build_user_status_description()).returning_last())
def test__build_user_status_description(user):
    """
    Tests whether ``build_user_status_description`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to render its status of.
    
    Returns
    -------
    description : `str`
    """
    return build_user_status_description(user)



def _iter_options__build_user_with_guild_profile_description():
    user_0 = User.precreate(
        236597320613888004,
        name = 'koishi',
    )
    
    user_1 = User.precreate(
        236597320613888005,
        name = 'koishi',
        display_name = 'koi',
        flags = UserFlag().update_by_keys(staff = True),
    )
    
    current_date = DateTime(2016, 10, 14, 21, 13, 46, tzinfo = TimeZone.utc)
    
    role_0 = Role.precreate(202308110000)
    role_1 = Role.precreate(202308110001)
    
    guild_profile = GuildProfile(
        joined_at = DateTime(2016, 10, 14, 21, 13, 27, tzinfo = TimeZone.utc),
        role_ids = [role_0.id, role_1.id],
        nick = 'koi',
        flags = GuildProfileFlag().update_by_keys(rejoined = True, onboarding_completed = True),
        boosts_since = DateTime(2016, 10, 14, 21, 13, 18, tzinfo = TimeZone.utc),
        timed_out_until = DateTime(2016, 10, 14, 21, 14, 46, tzinfo = TimeZone.utc),
    )

    # No guild profile
    yield (
        user_0,
        None,
        current_date,
        (
            f'Created: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
            f'Profile: <@{user_0.id}>\n'
            f'ID: {user_0.id}\n'
            f'\n'
            f'Joined: *none*\n'
            f'Roles: *none*'
        ),
    )
    
    # With guild profile
    yield (
        user_1,
        guild_profile,
        current_date,
        (
            f'Created: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
            f'Profile: <@{user_1.id}>\n'
            f'ID: {user_1.id}\n'
            f'Display name: koi\n'
            f'Flags: staff\n'
            f'\n'
            f'Joined: 2016-10-14 21:13:27 [*19 seconds ago*]\n'
            f'Roles: <@&202308110001>, <@&202308110000>\n'
            f'Nick: koi\n'
            f'Booster since: 2016-10-14 21:13:18 [*28 seconds*]\n'
            f'Timed out until: 2016-10-14 21:14:46 [*1 minute*]\n'
            f'Flags: onboarding completed, rejoined'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__build_user_with_guild_profile_description()).returning_last())
def test__build_user_with_guild_profile_description(user, guild_profile, current_date_time):
    """
    Tests whether ``build_user_with_guild_profile_description`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who joined or left.
    guild_profile : `None`, ``GuildProfile``
        The user's guild profile.
    current_date_time : `DateTime`
        The current time to use as a reference.
    
    Returns
    -------
    description : `str`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        build_user_with_guild_profile_description, 6, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    return mocked(user, guild_profile)
