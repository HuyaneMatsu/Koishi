import vampytest
from hata import (
    Color, Component, Icon, IconType, MediaInfo, MediaItem, User, create_button, create_media_gallery, create_row,
    create_section, create_separator, create_text_display, create_thumbnail_media
)

from ...user_stats_core import UserStats

from ..component_building import build_user_stats_primary_components


def _iter_options():
    user_id_0 = 202503120020
    user_id_1 = 202503120021
    
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
                create_text_display('# Satori\'s stats'),
                create_text_display(
                    'Housewife-capabilities: 5\n'
                    'Cuteness: 6\n'
                    'Bedroom-skills: 7\n'
                    'Charm: 8\n'
                    'Loyalty: 9'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id_1!s}/00000000000000000000000000000002.png'
                ),
            ),
            create_separator(
            ),
            create_media_gallery(
                MediaItem(
                    MediaInfo(
                        'https://mocked.stats.chart/'
                    )
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'View secondary stats & skills',
                    custom_id = f'user_stats.secondary.{user_id_0:x}.{user_id_1:x}'
                ),
            ),
        ],
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_stats_primary_components(user_id, target_user, user_stats, guild_id):
    """
    Tests whether ``build_user_stats_primary_components`` works as intended.
    
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
    get_user_stats_chart_url_called = False
    
    def mocked_get_user_stats_chart_url(input_user_stats, input_color):
        nonlocal user_stats
        nonlocal get_user_stats_chart_url_called
        
        vampytest.assert_instance(input_color, Color)
        vampytest.assert_is(user_stats, input_user_stats)
        get_user_stats_chart_url_called = True
        return 'https://mocked.stats.chart/'
    
    mocked = vampytest.mock_globals(
        build_user_stats_primary_components,
        get_user_stats_chart_url = mocked_get_user_stats_chart_url,
    )
    output = mocked(user_id, target_user, user_stats, guild_id)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    vampytest.assert_true(get_user_stats_chart_url_called)
    
    return output
