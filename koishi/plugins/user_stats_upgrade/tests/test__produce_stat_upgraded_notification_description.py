import vampytest
from hata import User

from ..content_building import produce_stat_upgraded_notification_description


def _iter_options():
    user = User.precreate(
        202511300002,
        name = 'Satori',
    )
    
    yield (
        5,
        5,
        4,
        6,
        9,
        0,
        0,
        2,
        1,
        0,
        user,
        0,
        (
            f'Satori upgraded your stats:\n'
            f'\n'
            f'- Bedroom-skills 4 -> 6\n'
            f'- Charm 6 -> 7'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_stat_upgraded_notification_description(
    stat_housewife,
    stat_cuteness,
    stat_bedroom,
    stat_charm,
    stat_loyalty,
    modify_housewife_by,
    modify_cuteness_by,
    modify_bedroom_by,
    modify_charm_by,
    modify_loyalty_by,
    source_user,
    guild_id,
):
    """
    Tests whether ``produce_stat_upgraded_notification_description`` works as intended..
    
    Parameters
    ----------
    stat_housewife : `int`
        The user's current housewife stat.
    
    stat_cuteness : `int`
        The user's current cuteness stat.
    
    stat_bedroom : `int`
        The user's current bedroom stat.
    
    stat_charm : `int`
        The user's current charm stat.
    
    stat_loyalty : `int`
        The user's current loyalty stat.
    
    modify_housewife_by : `int`
        The amount to modify the housewife stat by.
    
    modify_cuteness_by : `int`
        The amount to modify the cuteness stat by.
    
    modify_bedroom_by : `int`
        The amount to modify the bedroom stat by.
    
    modify_charm_by : `int`
        The amount to modify the charm stat by.
    
    modify_loyalty_by : `int`
        The amount to modify the loyalty stat by.
    
    source_user : ``ClientUserBase``
        The user upgrading the stats.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    ------
    output : `str`
    """
    output = [*produce_stat_upgraded_notification_description(
        stat_housewife,
        stat_cuteness,
        stat_bedroom,
        stat_charm,
        stat_loyalty,
        modify_housewife_by,
        modify_cuteness_by,
        modify_bedroom_by,
        modify_charm_by,
        modify_loyalty_by,
        source_user,
        guild_id,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
