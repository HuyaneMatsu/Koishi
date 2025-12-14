import vampytest
from hata import User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..content_building import produce_stat_upgrade_success_description


def _iter_options():
    user = User.precreate(
        202511300001,
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
        5650,
        5633,
        None,
        0,
        (
            f'You upgraded the following stats:\n'
            f'\n'
            f'- Bedroom-skills 4 -> 6\n'
            f'- Charm 6 -> 7\n'
            f'\n'
            f'Your {EMOJI__HEART_CURRENCY}:\n'
            f'```ansi\n'
            f'5650 \x1b[31m->\x1b[0m 17\n'
            f'```'
        ),
    )
    
    yield (
        5,
        5,
        5,
        5,
        5,
        1,
        0,
        0,
        0,
        0,
        5650,
        5633,
        user,
        0,
        (
            f'You upgraded the following stats of Satori:\n'
            f'\n'
            f'- Housewife-capabilities 5 -> 6\n'
            f'\n'
            f'Your {EMOJI__HEART_CURRENCY}:\n'
            f'```ansi\n'
            f'5650 \x1b[31m->\x1b[0m 17\n'
            f'```'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_stat_upgrade_success_description(
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
    current_balance,
    required_balance,
    target_user,
    guild_id,
):
    """
    Tests whether ``produce_stat_upgrade_success_description`` works as intended..
    
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
    
    current_balance : `int`
        The user's current balance.
    
    required_balance : `int`
        The required balance for upgrading.
    
    target_user : ``None | ClientUserBase``
        The targeted user if any.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    ------
    output : `str`
    """
    output = [*produce_stat_upgrade_success_description(
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
        current_balance,
        required_balance,
        target_user,
        guild_id,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
