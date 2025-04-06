import vampytest

from hata import GuildProfile, ICON_TYPE_ANIMATED, ICON_TYPE_STATIC, Icon, User

from ..constants import (
    ICON_SOURCE_DEFAULT, ICON_SOURCE_GLOBAL, ICON_SOURCE_GUILD, ICON_SOURCE_LOCAL
)
from ..icon_helpers import get_banner_of


def _iter_options():
    user_id_0 = 202408190012
    user_id_1 = 202408190013
    
    guild_id_0 = 202408190012
    guild_id_1 = 202408190013
    
    user_0 = User.precreate(user_id_0)
    user_0.guild_profiles[guild_id_0] = GuildProfile()
    
    user_1 = User.precreate(user_id_1, banner = Icon(ICON_TYPE_STATIC, 2))
    user_1.guild_profiles[guild_id_1] = GuildProfile(banner = Icon(ICON_TYPE_ANIMATED, 3))
    
    
    yield (
        user_0,
        0,
        ICON_SOURCE_DEFAULT,
        None,
    )
    yield (
        user_0,
        guild_id_0,
        ICON_SOURCE_DEFAULT,
        None,
    )
    yield (
        user_0,
        guild_id_1,
        ICON_SOURCE_DEFAULT,
        None,
    )
    yield (
        user_0,
        0,
        ICON_SOURCE_GLOBAL,
        None,
    )
    yield (
        user_0,
        guild_id_0,
        ICON_SOURCE_GLOBAL,
        None,
    )
    yield (
        user_0,
        guild_id_1,
        ICON_SOURCE_GLOBAL,
        None,
    )
    yield (
        user_0,
        0,
        ICON_SOURCE_GUILD,
        None,
    )
    yield (
        user_0,
        guild_id_0,
        ICON_SOURCE_GUILD,
        None,
    )
    yield (
        user_0,
        guild_id_1,
        ICON_SOURCE_GUILD,
        None,
    )
    yield (
        user_0,
        0,
        ICON_SOURCE_LOCAL,
        None,
    )
    yield (
        user_0,
        guild_id_0,
        ICON_SOURCE_LOCAL,
        None,
    )
    yield (
        user_0,
        guild_id_1,
        ICON_SOURCE_LOCAL,
        None,
    )
    
    yield (
        user_1,
        0,
        ICON_SOURCE_DEFAULT,
        None,
    )
    yield (
        user_1,
        guild_id_0,
        ICON_SOURCE_DEFAULT,
        None,
    )
    yield (
        user_1,
        guild_id_1,
        ICON_SOURCE_DEFAULT,
        None,
    )
    yield (
        user_1,
        0,
        ICON_SOURCE_GLOBAL,
        f'https://cdn.discordapp.com/banners/{user_id_1}/00000000000000000000000000000002.png?size=4096',
    )
    yield (
        user_1,
        guild_id_0,
        ICON_SOURCE_GLOBAL,
        f'https://cdn.discordapp.com/banners/{user_id_1}/00000000000000000000000000000002.png?size=4096',
    )
    yield (
        user_1,
        guild_id_1,
        ICON_SOURCE_GLOBAL,
        f'https://cdn.discordapp.com/banners/{user_id_1}/00000000000000000000000000000002.png?size=4096',
    )
    yield (
        user_1,
        0,
        ICON_SOURCE_GUILD,
        None,
    )
    yield (
        user_1,
        guild_id_0,
        ICON_SOURCE_GUILD,
        None,
    )
    yield (
        user_1,
        guild_id_1,
        ICON_SOURCE_GUILD,
        f'https://cdn.discordapp.com/guilds/{guild_id_1}/users/{user_id_1}/banners/a_00000000000000000000000000000003.gif?size=4096',
    )
    yield (
        user_1,
        0,
        ICON_SOURCE_LOCAL,
        f'https://cdn.discordapp.com/banners/{user_id_1}/00000000000000000000000000000002.png?size=4096',
    )
    yield (
        user_1,
        guild_id_0,
        ICON_SOURCE_LOCAL,
        f'https://cdn.discordapp.com/banners/{user_id_1}/00000000000000000000000000000002.png?size=4096',
    )
    yield (
        user_1,
        guild_id_1,
        ICON_SOURCE_LOCAL,
        f'https://cdn.discordapp.com/guilds/{guild_id_1}/users/{user_id_1}/banners/a_00000000000000000000000000000003.gif?size=4096',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_banner_of(user, guild_id, icon_source):
    """
    Tests whether ``get_banner_of`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    guild_id : `int`
        The context's guild's identifier.
    icon_source : `int`
        From which source should be the icon taken from.
    
    Returns
    -------
    output : `None | str`
    """
    output = get_banner_of(user, guild_id, icon_source)
    vampytest.assert_instance(output, str, nullable = True)
    return output
