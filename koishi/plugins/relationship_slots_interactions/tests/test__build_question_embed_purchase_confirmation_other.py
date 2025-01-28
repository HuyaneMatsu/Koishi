import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_question_embed_purchase_confirmation_other


def _iter_options():
    user_id = 202501260001
    guild_id = 202501260002
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    
    yield (
        2000,
        3,
        user,
        0,
        Embed(
            'Confirm your purchase',
            (
                f'Are you sure you want to buy Keine\'s 3rd relationship slot for '
                f'2000 {EMOJI__HEART_CURRENCY}?'
            ),
        ),
    )
    
    yield (
        2000,
        3,
        user,
        guild_id,
        Embed(
            'Confirm your purchase',
            (
                f'Are you sure you want to buy Caver\'s 3rd relationship slot for '
                f'2000 {EMOJI__HEART_CURRENCY}?'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_question_embed_purchase_confirmation_other(
    required_balance, new_relationship_slot_count, user, guild_id
):
    """
    Tests whether ``build_question_embed_purchase_confirmation_other`` works as intended.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to buy the relationship slot.
    
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_question_embed_purchase_confirmation_other(
        required_balance, new_relationship_slot_count, user, guild_id
    )
    vampytest.assert_instance(output, Embed)
    return output
