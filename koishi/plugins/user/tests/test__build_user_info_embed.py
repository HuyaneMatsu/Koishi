from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Color, Embed, GuildProfile, ICON_TYPE_ANIMATED, ICON_TYPE_STATIC, Icon, Role, User

from ..embed_builders import build_user_info_embed

from .mocks import DateTimeMock, is_instance_mock


def _iter_options():
    user_id = 202408190030
    
    user_name = 'Marisa'
    
    guild_id = 202408190032
    
    role_id = 202408190034
    
    role_color = Color(123)
    
    user = User.precreate(user_id, avatar = Icon(ICON_TYPE_STATIC, 2), name = user_name)
    user.guild_profiles[guild_id] = GuildProfile(
        avatar = Icon(ICON_TYPE_ANIMATED, 3),
        joined_at = DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc),
        role_ids = [role_id],
    )
    
    role = Role.precreate(role_id, color = role_color)
    
    
    yield (
        user,
        0,
        [role],
        DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc),
        Embed(
            f'{user_name!s}',
            color = None,
        ).add_field(
            'User information',
            (
                f'Created: 2015-01-01 00:00:48 [*1 year, 9 months, 13 days ago*]\n'
                f'Profile: <@{202408190030!s}>\n'
                f'ID: {202408190030!s}'
            ),
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id}/00000000000000000000000000000002.png',
        ),
    )
    
    yield (
        user,
        guild_id,
        [role],
        DateTime(2016, 10, 14, 21, 13, 36, tzinfo = TimeZone.utc),
        Embed(
            f'{user_name!s}',
            color = role_color,
        ).add_field(
            'User information',
            (
                f'Created: 2015-01-01 00:00:48 [*1 year, 9 months, 13 days ago*]\n'
                f'Profile: <@{202408190030!s}>\n'
                f'ID: {202408190030!s}'
            ),
        ).add_field(
            'In guild profile',
            (
                f'Joined: 2016-05-14 00:00:00 [*5 months, 21 hours, 13 minutes ago*]\n'
                f'Roles: <@&{role_id!s}>'
            ),
        ).add_thumbnail(
            f'https://cdn.discordapp.com/guilds/{guild_id}/users/{user_id}/avatars/a_00000000000000000000000000000003.gif',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_info_embed(user, guild_id, extra, current_date_time):
    """
    Tests whether ``build_user_info_embed`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    guild_id : `int`
        The context's guild's identifier.
    extra : `list`
        Additional objects to keep in the cache.
    current_date_time : `DateTime`
        The current time to use as a reference.
    
    Returns
    -------
    output : ``Embed``
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        build_user_info_embed, 6, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    output = mocked(user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
