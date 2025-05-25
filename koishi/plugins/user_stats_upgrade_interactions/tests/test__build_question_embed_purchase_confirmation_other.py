import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_question_embed_purchase_confirmation_other


def _iter_options():
    user = User.precreate(202503150002, name = 'Sariel')
    guild_id = 202503150003
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Angel')
    
    yield (
        2000,
        2,
        12,
        user,
        0,
        Embed(
            'Stat upgrade',
            (
                f'Are you sure to upgrade Sariel\'s bedroom skills to 12 for '
                f'2000 {EMOJI__HEART_CURRENCY}?'
            )
        )
    )
    
    yield (
        2000,
        2,
        12,
        user,
        guild_id,
        Embed(
            'Stat upgrade',
            (
                f'Are you sure to upgrade Angel\'s bedroom skills to 12 for '
                f'2000 {EMOJI__HEART_CURRENCY}?'
            )
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_question_embed_purchase_confirmation_other(
    required_balance, stat_index, stat_value_after, user, guild_id
):
    """
    Tests whether ``build_question_embed_purchase_confirmation_other`` works as intended.
    
    Parameters
    ----------
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
    output = build_question_embed_purchase_confirmation_other(
        required_balance, stat_index, stat_value_after, user, guild_id
    )
    vampytest.assert_instance(output, Embed)
    return output
