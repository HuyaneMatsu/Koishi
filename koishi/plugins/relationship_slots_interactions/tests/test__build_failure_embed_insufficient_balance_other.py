import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_failure_embed_insufficient_balance_other


def _iter_options():
    user_id = 202501270000
    guild_id = 202501270001
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    
    
    yield (
        2000,
        3,
        user,
        0,
        Embed(
            'Insufficient balance',
            (
                'You do not have enough available heart to buy more relationship slots for Keine.\n'
                f'You need 2000 {EMOJI__HEART_CURRENCY} to buy the 3rd slot.'
            ),
        ),
    )
    
    yield (
        2000,
        3,
        user,
        guild_id,
        Embed(
            'Insufficient balance',
            (
                'You do not have enough available heart to buy more relationship slots for Caver.\n'
                f'You need 2000 {EMOJI__HEART_CURRENCY} to buy the 3rd slot.'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_insufficient_balance_other(required_balance, new_relationship_slot_count, user, guild_id):
    """
    Tests whether ``build_failure_embed_insufficient_balance_other`` works as intended.
    
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
    output = build_failure_embed_insufficient_balance_other(
        required_balance, new_relationship_slot_count, user, guild_id
    )
    vampytest.assert_instance(output, Embed)
    return output
