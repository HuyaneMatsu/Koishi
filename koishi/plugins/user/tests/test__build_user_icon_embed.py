import vampytest
from hata import Color, Embed, GuildProfile, ICON_TYPE_ANIMATED, ICON_TYPE_STATIC, Icon, Role, User

from ..constants import (
    ICON_KIND_AVATAR, ICON_KIND_BANNER, ICON_SOURCE_DEFAULT, ICON_SOURCE_GLOBAL, ICON_SOURCE_GUILD, ICON_SOURCE_LOCAL
)
from ..embed_builders import build_user_icon_embed


def _iter_options():
    user_id_0 = 202408190030
    user_id_1 = 202408190031
    
    user_name_0 = 'Marisa'
    user_name_1 = 'Youmu'
    
    guild_id_0 = 202408190032
    guild_id_1 = 202408190033
    
    role_id_0 = 202408190034
    role_id_1 = 202408190035
    
    role_color_0 = Color(123)
    role_color_1 = Color(456)
    
    user_0 = User.precreate(user_id_0, avatar = Icon(ICON_TYPE_STATIC, 2), name = user_name_0)
    user_0.guild_profiles[guild_id_0] = GuildProfile(avatar = Icon(ICON_TYPE_ANIMATED, 3), role_ids = [role_id_0])
    
    user_1 = User.precreate(user_id_1, banner = Icon(ICON_TYPE_STATIC, 2), name = user_name_1)
    user_1.guild_profiles[guild_id_1] = GuildProfile(banner = Icon(ICON_TYPE_ANIMATED, 3), role_ids = [role_id_1])
    
    role_0 = Role.precreate(role_id_0, color = role_color_0)
    role_1 = Role.precreate(role_id_1, color = role_color_1)
    
    
    
    yield (
        user_0,
        0,
        ICON_KIND_AVATAR,
        ICON_SOURCE_DEFAULT,
        [role_0, role_1],
        Embed(
            f'{user_name_0}\'s default avatar',
            color = None,
            url = f'https://cdn.discordapp.com/embed/avatars/5.png',
        ).add_image(
            f'https://cdn.discordapp.com/embed/avatars/5.png',
        ),
    )
    
    yield (
        user_0,
        guild_id_0,
        ICON_KIND_AVATAR,
        ICON_SOURCE_LOCAL,
        [role_0, role_1],
        Embed(
            f'{user_name_0}\'s local avatar',
            color = role_color_0,
            url = f'https://cdn.discordapp.com/guilds/{guild_id_0}/users/{user_id_0}/avatars/a_00000000000000000000000000000003.gif?size=4096'
        ).add_image(
            f'https://cdn.discordapp.com/guilds/{guild_id_0}/users/{user_id_0}/avatars/a_00000000000000000000000000000003.gif?size=4096',
        )
    )
    
    yield (
        user_0,
        guild_id_1,
        ICON_KIND_AVATAR,
        ICON_SOURCE_LOCAL,
        [role_0, role_1],
        Embed(
            f'{user_name_0}\'s local avatar',
            color = None,
            url = f'https://cdn.discordapp.com/avatars/{user_id_0}/00000000000000000000000000000002.png?size=4096',
        ).add_image(
            f'https://cdn.discordapp.com/avatars/{user_id_0}/00000000000000000000000000000002.png?size=4096',
        ),
    )

    
    yield (
        user_1,
        0,
        ICON_KIND_BANNER,
        ICON_SOURCE_DEFAULT,
        [role_0, role_1],
        Embed(
            f'{user_name_1}\'s default banner',
            color = None,
            url = None,
        ).add_footer(
            'The user has no default banner.'
        ),
    )
    
    yield (
        user_1,
        guild_id_0,
        ICON_KIND_BANNER,
        ICON_SOURCE_LOCAL,
        [role_0, role_1],
        Embed(
            f'{user_name_1}\'s local banner',
            color = None,
            url = f'https://cdn.discordapp.com/banners/{user_id_1}/00000000000000000000000000000002.png?size=4096',
        ).add_image(
            f'https://cdn.discordapp.com/banners/{user_id_1}/00000000000000000000000000000002.png?size=4096',
        ),
    )
    
    yield (
        user_1,
        guild_id_1,
        ICON_KIND_BANNER,
        ICON_SOURCE_LOCAL,
        [role_0, role_1],
        Embed(
            f'{user_name_1}\'s local banner',
            color = role_color_1,
            url = f'https://cdn.discordapp.com/guilds/{guild_id_1}/users/{user_id_1}/banners/a_00000000000000000000000000000003.gif?size=4096',
        ).add_image(
            f'https://cdn.discordapp.com/guilds/{guild_id_1}/users/{user_id_1}/banners/a_00000000000000000000000000000003.gif?size=4096',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_icon_embed(user, guild_id, icon_kind, icon_source, extra):
    """
    Tests whether ``build_user_icon_embed`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    guild_id : `int`
        The context's guild's identifier.
    icon_kind : `int`
        Which icon should be taken of the user.
    icon_source : `int`
        From which source should be the icon taken from.
    extra : `list`
        Additional objects to keep in the cache.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_user_icon_embed(user, guild_id, icon_kind, icon_source)
    vampytest.assert_instance(output, Embed)
    return output
