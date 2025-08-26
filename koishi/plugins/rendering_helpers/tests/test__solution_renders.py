from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import (
    Activity, ActivityAssets, ActivityFlag, ActivityParty, ActivitySecrets, ActivityTimestamps, ActivityType,
    BUILTIN_EMOJIS, HangType, GuildProfile, GuildProfileFlag, Role, Status, StatusByPlatform, User, UserFlag
)

from ..constants import GUILD_PROFILE_RENDER_MODE_GENERAL, GUILD_PROFILE_RENDER_MODE_JOIN, GUILD_PROFILE_RENDER_MODE_LEAVE
from ..solution_renderers import (
    render_activity_description_into, render_guild_profile_description_into,
    render_nullable_guild_profile_description_into, render_nulled_guild_profile_description_into,
    render_user_description_into, render_user_status_description_into
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
        DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc),
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
        DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc),
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
        DateTime(2016, 10, 14, 21, 13, 46, tzinfo = TimeZone.utc),
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
        GUILD_PROFILE_RENDER_MODE_GENERAL,
        DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc),
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
        GUILD_PROFILE_RENDER_MODE_GENERAL,
        DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc),
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
            timed_out_until = DateTime(2016, 10, 14, 21, 12, 46, tzinfo = TimeZone.utc),
        ),
        GUILD_PROFILE_RENDER_MODE_GENERAL,
        DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc),
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
            joined_at = DateTime(2016, 10, 14, 21, 13, 17, tzinfo = TimeZone.utc),
            role_ids = [role_0.id, role_1.id],
            nick = 'koi',
            flags = GuildProfileFlag().update_by_keys(rejoined = True, onboarding_completed = True),
            boosts_since = DateTime(2016, 10, 14, 21, 13, 18, tzinfo = TimeZone.utc),
            timed_out_until = DateTime(2016, 10, 14, 21, 14, 46, tzinfo = TimeZone.utc),
        ),
        GUILD_PROFILE_RENDER_MODE_GENERAL,
        DateTime(2016, 10, 14, 21, 13, 46, tzinfo = TimeZone.utc),
        (
            (
                f'Joined: 2016-10-14 21:13:17 [*29 seconds ago*]\n'
                f'Roles: <@&{role_1.id}>, <@&{role_0.id}>\n'
                f'Nick: koi\n'
                f'Booster since: 2016-10-14 21:13:18 [*28 seconds*]\n'
                f'Timed out until: 2016-10-14 21:14:46 [*1 minute*]\n'
                f'Flags: onboarding completed, rejoined'
            ),
            True,
        )
    )

    # Join with roles

    yield (
        False,
        GuildProfile(
            joined_at = DateTime(2016, 10, 14, 21, 13, 17, tzinfo = TimeZone.utc),
            role_ids = [role_0.id, role_1.id],
        ),
        GUILD_PROFILE_RENDER_MODE_JOIN,
        DateTime(2016, 10, 14, 21, 13, 46, tzinfo = TimeZone.utc),
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
            joined_at = DateTime(2016, 10, 14, 21, 13, 17, tzinfo = TimeZone.utc),
            role_ids = None,
        ),
        GUILD_PROFILE_RENDER_MODE_JOIN,
        DateTime(2016, 10, 14, 21, 13, 46, tzinfo = TimeZone.utc),
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
            joined_at = DateTime(2016, 10, 14, 21, 13, 17, tzinfo = TimeZone.utc),
            role_ids = [role_0.id, role_1.id],
        ),
        GUILD_PROFILE_RENDER_MODE_LEAVE,
        DateTime(2016, 10, 14, 21, 13, 46, tzinfo = TimeZone.utc),
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
            joined_at = DateTime(2016, 10, 14, 21, 13, 17, tzinfo = TimeZone.utc),
            role_ids = None
        ),
        GUILD_PROFILE_RENDER_MODE_LEAVE,
        DateTime(2016, 10, 14, 21, 13, 46, tzinfo = TimeZone.utc),
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
    current_date = DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc)
    
    # General
    yield (
        False,
        GUILD_PROFILE_RENDER_MODE_GENERAL,
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
        GUILD_PROFILE_RENDER_MODE_GENERAL,
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
        GUILD_PROFILE_RENDER_MODE_JOIN,
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
        GUILD_PROFILE_RENDER_MODE_JOIN,
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
        GUILD_PROFILE_RENDER_MODE_LEAVE,
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
        GUILD_PROFILE_RENDER_MODE_LEAVE,
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
    current_date = DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc)
    
    yield (
        False,
        None,
        GUILD_PROFILE_RENDER_MODE_LEAVE,
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
            joined_at = DateTime(2016, 10, 14, 21, 13, 7, tzinfo = TimeZone.utc)
        ),
        GUILD_PROFILE_RENDER_MODE_LEAVE,
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


def _iter_options__render_activity_description_into():
    current_date = DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc)
    emoji = BUILTIN_EMOJIS['heart']
    
    # Minimal
    yield (
        False,
        Activity('with Kokoro'),
        current_date,
        (
            (
                f'Type: playing ~ 0\n'
                f'Name: with Kokoro'
            ),
            True,
        )
    )
    
    # Field already added
    yield (
        True,
        Activity('with Kokoro'),
        current_date,
        (
            (
                f'\n'
                f'Type: playing ~ 0\n'
                f'Name: with Kokoro'
            ),
            True,
        )
    )
    
    # Maximal
    yield (
        False,
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
            buttons = ['Rumia', 'Letty'],
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
                f'Buttons: \'Rumia\', \'Letty\'\n'
                f'Sync id: Mr. spider\n'
                f'Session id: Orin\n'
                f'Flags: embedded, play\n'
                f'Application id: 202308080001\n'
                f'Id: 202308080000\n'
                f'Created at: 2016-10-14 21:13:26 [*10 seconds ago*]'
            ),
            True,
        )
    )
    
    # Custom
    yield (
        False,
        Activity(
            activity_type = ActivityType.custom,
            created_at = DateTime(2016, 10, 14, 21, 13, 26, tzinfo = TimeZone.utc),
            emoji = emoji,
            state = 'Koishi Love!'
        ),
        current_date,
        (
            (
                f'Type: custom ~ 4\n'
                f'Emoji: {emoji.name} ({emoji.id!s})\n'
                f'State: Koishi Love!\n'
                f'Created at: 2016-10-14 21:13:26 [*10 seconds ago*]'
            ),
            True,
        )
    )
    
    # Hanging
    yield (
        False,
        Activity(
            activity_type = ActivityType.hanging,
            hang_type = HangType.focusing,
            created_at = DateTime(2016, 10, 14, 21, 13, 26, tzinfo = TimeZone.utc),
            emoji = emoji,
            details = 'Koishi Love!'
        ),
        current_date,
        (
            (
                f'Type: hanging ~ 6\n'
                f'Hang type: focusing ~ focusing\n'
                f'Emoji: {emoji.name} ({emoji.id!s})\n'
                f'Details: Koishi Love!\n'
                f'Created at: 2016-10-14 21:13:26 [*10 seconds ago*]'
            ),
            True,
        )
    )


@vampytest._(vampytest.call_from(_iter_options__render_activity_description_into()).returning_last())
def test__render_activity_description_into(field_added, activity, current_date_time):
    """
    Tests whether ``render_activity_description_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether there were fields added already.
    activity : ``Activity``
        The activity to render.
    current_date_time : `DateTime`
        The current time to use as a reference.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        render_activity_description_into, 4, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    into, field_added = mocked([], field_added, activity)
    return ''.join(into), field_added


def _iter_options__render_user_status_description_into():
    user_0 = User()
    
    user_1 = User()
    user_1.status = Status.idle
    user_1.status_by_platform = StatusByPlatform(
        desktop = Status.dnd,
        mobile = Status.idle,
        web = Status.online,
    )
    
    # minimal
    yield (
        False,
        user_0,
        (
            (
                f'Status: offline'
            ),
            True,
        )
    )
    
    # Field already added
    yield (
        True,
        user_0,
        (
            (
                f'\n'
                f'Status: offline'
            ),
            True,
        )
    )
    
    # Maximal
    yield (
        False,
        user_1,
        (
            (
                f'Status: idle\n'
                f'- Desktop: dnd\n'
                f'- Mobile: idle\n'
                f'- Web: online'
            ),
            True,
        )
    )


@vampytest._(vampytest.call_from(_iter_options__render_user_status_description_into()).returning_last())
def test__render_user_status_description_into(field_added, user):
    """
    Tests whether ``render_user_status_description_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether there were fields added already.
    user : ``ClientUserBase``
        The user to render its status of.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    into, field_added = render_user_status_description_into([], field_added, user)
    return ''.join(into), field_added
