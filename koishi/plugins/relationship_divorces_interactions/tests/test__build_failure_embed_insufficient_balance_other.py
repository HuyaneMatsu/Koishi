import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_failure_embed_insufficient_balance_other


def _iter_options():
    user_id = 202502050000
    guild_id = 202502050001
    
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
                'You do not have enough available hearts to hire ninjas to locate and burn the divorce papers of Keine.\n'
                f'You need 2000 {EMOJI__HEART_CURRENCY} to locate and burn the 3rd divorce papers.'
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
                'You do not have enough available hearts to hire ninjas to locate and burn the divorce papers of Caver.\n'
                f'You need 2000 {EMOJI__HEART_CURRENCY} to locate and burn the 3rd divorce papers.'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_insufficient_balance_other(required_balance, relationship_divorce_count, user, guild_id):
    """
    Tests whether ``build_failure_embed_insufficient_balance_other`` works as intended.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to locate and burn the divorce papers.
    
    relationship_divorce_count : `int`
        The relationship divorce count.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_insufficient_balance_other(
        required_balance, relationship_divorce_count, user, guild_id
    )
    vampytest.assert_instance(output, Embed)
    return output
