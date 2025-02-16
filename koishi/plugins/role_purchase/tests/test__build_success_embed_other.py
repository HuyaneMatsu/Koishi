import vampytest
from hata import Embed, GuildProfile, Role, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_success_embed_other


def _iter_options():
    role_id = 202502130014
    guild_id = 202502130015
    user_id = 202502130016
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver', role_ids = [role_id])
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    
    yield (
        role,
        3000,
        1000,
        user,
        0,
        Embed(
            'Successful purchase',
            f'You successfully purchased the Nyan role for Keine.',
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```\n'
                f'3000 -> 2000\n'
                f'```'
            ),
        ),
    )
    
    yield (
        role,
        3000,
        1000,
        user,
        guild_id,
        Embed(
            'Successful purchase',
            f'You successfully purchased the Nyan role for Caver.',
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```\n'
                f'3000 -> 2000\n'
                f'```'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_other(role, balance, required_balance, user, guild_id):
    """
    Tests whether ``build_success_embed_other`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The purchased role.
    
    balance : `int`
        The user's balance.
    
    required_balance : `int`
        Required balance for the role.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed_other(role, balance, required_balance, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
