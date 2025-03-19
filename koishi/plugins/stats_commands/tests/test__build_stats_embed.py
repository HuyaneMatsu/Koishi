import vampytest
from hata import Color, Embed, GuildProfile, User

from ...stats_core import Stats

from ..embed_builders import build_stats_embed


def _iter_options():
    user_id = 202503120020
    guild_id = 202503120021
    
    stats = Stats(user_id)
    stats.stat_housewife = 5
    stats.stat_cuteness = 6
    stats.stat_bedroom = 7
    stats.stat_charm = 8
    stats.stat_loyalty = 9
    
    user = User.precreate(user_id, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        stats,
        user,
        0,
        Embed(
            'Satori\'s stats',
            'mocked description',
            color = Color(0x3eac8d),
        ).add_image(
            'https://mocked.stats.chart/',
        ),
    )
    
    yield (
        stats,
        user,
        guild_id,
        Embed(
            'Sato\'s stats',
            'mocked description',
            color = Color(0x3eac8d),
        ).add_image(
            'https://mocked.stats.chart/',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_stats_embed(stats, user, guild_id):
    """
    Parameters
    ----------
    stats : ``Stats``
        The user's stats.
    
    user : ``ClientUserBase``
        The stats.
    
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    get_stats_description_called = False
    get_stats_chart_url_called = False
    
    def mocked_get_stats_description(input_stats):
        nonlocal get_stats_description_called
        nonlocal stats
        
        vampytest.assert_is(stats, input_stats)
        get_stats_description_called = True
        return 'mocked description'
    
    def mocked_get_stats_chart_url(input_stats, input_color):
        nonlocal stats
        nonlocal get_stats_chart_url_called
        
        vampytest.assert_instance(input_color, Color)
        vampytest.assert_is(stats, input_stats)
        get_stats_chart_url_called = True
        return 'https://mocked.stats.chart/'
    
    mocked = vampytest.mock_globals(
        build_stats_embed,
        get_stats_description = mocked_get_stats_description,
        get_stats_chart_url = mocked_get_stats_chart_url,
    )
    output = mocked(stats, user, guild_id)
    vampytest.assert_instance(output, Embed)
    
    vampytest.assert_true(get_stats_description_called)
    vampytest.assert_true(get_stats_chart_url_called)
    
    return output
