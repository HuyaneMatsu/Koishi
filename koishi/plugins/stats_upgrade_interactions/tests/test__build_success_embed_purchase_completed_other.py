import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...balance_rendering.constants import COLOR_CODE_RED, COLOR_CODE_RESET

from ..embed_builders import build_success_embed_purchase_completed_other


def _iter_options():
    user = User.precreate(202503150004, name = 'Sariel')
    guild_id = 202503150005
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Angel')
    
    yield (
        2000,
        1000,
        2,
        13,
        user,
        0,
        Embed(
            'Purchase successful',
            f'You upgraded Sariel\'s bedroom skills to 13.',
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```ansi\n'
                f'2000 {COLOR_CODE_RED}->{COLOR_CODE_RESET} 1000\n'
                f'```'
            ),
            True,
        ),
    )
    
    yield (
        2000,
        1000,
        2,
        13,
        user,
        guild_id,
        Embed(
            'Purchase successful',
            f'You upgraded Angel\'s bedroom skills to 13.',
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```ansi\n'
                f'2000 {COLOR_CODE_RED}->{COLOR_CODE_RESET} 1000\n'
                f'```'
            ),
            True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_purchase_completed_other(
    balance_before, required_balance, stat_index, stat_value_after, user, guild_id
):
    """
    Tests whether ``build_success_embed_purchase_completed_other`` works as intended.
    
    Parameters
    ----------
    balance_before : `int`
        The user's balance before its purchase.
    
    required_balance : `int`
        The required amount of balance for the purchase.
    
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
    output = build_success_embed_purchase_completed_other(
        balance_before, required_balance, stat_index, stat_value_after, user, guild_id
    )
    vampytest.assert_instance(output, Embed)
    return output
