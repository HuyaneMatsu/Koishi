import vampytest
from hata import InteractionForm, User, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..component_building import build_confirmation_form


def _iter_options():
    user = User.precreate(
        202511300004,
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
        5633,
        None,
        0,
        InteractionForm(
            'Confirm stat upgrading',
            [
                create_text_display(
                    f'Are you sure to upgrade the following stats?\n'
                    f'\n'
                    f'- Bedroom-skills 4 -> 6\n'
                    f'- Charm 6 -> 7\n'
                    f'\n'
                    f'It will cost you 5633 {EMOJI__HEART_CURRENCY}.'
                ),
            ],
            f'user.stats_upgrade.{0:x}.{0:x}.{2:x}.{1:x}.{0:x}.{0:x}',
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
        5633,
        user,
        0,
        InteractionForm(
            'Confirm stat upgrading',
            [
                create_text_display(
                    f'Are you sure to upgrade the following stats of Satori?\n'
                    f'\n'
                    f'- Housewife-capabilities 5 -> 6\n'
                    f'\n'
                    f'It will cost you 5633 {EMOJI__HEART_CURRENCY}.'
                ),
            ],
            f'user.stats_upgrade.{1:x}.{0:x}.{0:x}.{0:x}.{0:x}.{user.id:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_confirmation_form(
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
    required_balance,
    target_user,
    guild_id,
):
    """
    Tests whether ``build_confirmation_form`` works as intended..
    
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
    
    required_balance : `int`
        The required balance for upgrading.
    
    target_user : ``None | ClientUserBase``
        The targeted user if any.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    ------
    output : ``InteractionForm``
    """
    output = build_confirmation_form(
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
        required_balance,
        target_user,
        guild_id,
    )
    vampytest.assert_instance(output, InteractionForm)
    return output
