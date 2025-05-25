import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_failure_embed_insufficient_available_balance_other


def _iter_options():
    user = User.precreate(202503150000, name = 'Sariel')
    guild_id = 202503150001
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Angel')
    
    yield (
        2000,
        1000,
        2,
        12,
        user,
        0,
        Embed(
            'Insufficient available balance',
            (
                f'You cannot upgrade Sariel\'s bedroom skills to 12 because you have only '
                f'1000 available {EMOJI__HEART_CURRENCY} which is lower than the required '
                f'2000 {EMOJI__HEART_CURRENCY}.'
            )
        )
    )
    
    yield (
        2000,
        1000,
        2,
        12,
        user,
        guild_id,
        Embed(
            'Insufficient available balance',
            (
                f'You cannot upgrade Angel\'s bedroom skills to 12 because you have only '
                f'1000 available {EMOJI__HEART_CURRENCY} which is lower than the required '
                f'2000 {EMOJI__HEART_CURRENCY}.'
            )
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_insufficient_available_balance_other(
    required_balance, available_balance, stat_index, stat_value_after, user, guild_id
):
    """
    Tests whether ``build_failure_embed_insufficient_available_balance_other`` works as intended.
    
    Parameters
    ----------
    required_balance : `int`
        The required amount of balance for the purchase.
    
    available_balance : `int`
        Available balance.
    
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The current guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_insufficient_available_balance_other(
        required_balance, available_balance, stat_index, stat_value_after, user, guild_id
    )
    vampytest.assert_instance(output, Embed)
    return output
