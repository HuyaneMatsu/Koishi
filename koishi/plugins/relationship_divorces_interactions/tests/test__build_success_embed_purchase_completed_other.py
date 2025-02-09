import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_success_embed_purchase_completed_other


def _iter_options():
    user_id = 202502050006
    guild_id = 202502050007
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    
    yield (
        2000,
        3,
        user,
        0,
        Embed(
            'Purchase successful',
            (
                f'You sent out your hired ninjas to locate and burn Keine\'s 3rd divorce papers for '
                f'2000 {EMOJI__HEART_CURRENCY}.\n'
                f'They completed the task splendid; the case is cool even in the summer.'
            ),
        )
    )
    
    yield (
        2000,
        3,
        user,
        guild_id,
        Embed(
            'Purchase successful',
            (
                f'You sent out your hired ninjas to locate and burn Caver\'s 3rd divorce papers for '
                f'2000 {EMOJI__HEART_CURRENCY}.\n'
                f'They completed the task splendid; the case is cool even in the summer.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_purchase_completed_other(required_balance, relationship_divorce_count, user, guild_id):
    """
    Tests whether ``build_success_embed_purchase_completed_other`` works as intended.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to locate and burn the divorce papers.
    
    relationship_divorce_count : `int`
        The current relationship divorce count.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed_purchase_completed_other(required_balance, relationship_divorce_count, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
