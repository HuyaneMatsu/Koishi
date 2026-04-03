import vampytest
from hata import (
    Component, Icon, IconType, User, create_button, create_row, create_section, create_separator, create_text_display,
    create_thumbnail_media
)

from ...user_stats_core import UserStats

from ..component_building import build_user_stats_secondary_components


def _iter_options():
    user_id_0 = 202512270013
    user_id_1 = 202512270014
    
    stats = UserStats(user_id_1)
    stats.stat_housewife = 5
    stats.stat_cuteness = 6
    stats.stat_bedroom = 7
    stats.stat_charm = 8
    stats.stat_loyalty = 9
    
    target_user = User.precreate(
        user_id_1,
        avatar = Icon(IconType.static, 2),
        name = 'Satori',
    )
    
    yield (
        user_id_0,
        target_user,
        stats,
        0,
        [
            create_section(
                create_text_display('# Satori\'s secondary stats & skills'),
                create_text_display(
                    'Health: 176\n'
                    'Energy: 166\n'
                    'Movement: 1.1 (m/s)\n'
                    'Inventory: 41.250 (kg)\n'
                    '\n'
                    'Butchering: 15 (+18%)\n'
                    'Fishing: 17 (+23%)\n'
                    'Foraging: 16 (+20%)\n'
                    'Gardening: 16 (+20%)\n'
                    'Hunting: 18 (+26%)'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id_1!s}/00000000000000000000000000000002.png'
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'View primary stats',
                    custom_id = f'user_stats.primary.{user_id_0:x}.{user_id_1:x}'
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_stats_secondary_components(user_id, target_user, user_stats, guild_id):
    """
    Tests whether ``build_user_stats_secondary_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    target_user : ``ClientUserBase``
        The user who's stats are shown.
    
    user_stats : ``UserStats``
        The user's stats.
    
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_user_stats_secondary_components(user_id, target_user, user_stats, guild_id)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
