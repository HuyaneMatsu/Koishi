import vampytest
from hata import Embed, Role

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_success_embed_self


def _iter_options():
    role_id = 202502130013
    guild_id = 202502130014
    
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    
    yield (
        role,
        3000,
        1000,
        Embed(
            'Successful purchase',
            f'You successfully purchased the Nyan role.',
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
def test__build_success_embed_self(role, balance, required_balance):
    """
    Tests whether ``build_success_embed_self`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The purchased role.
    
    balance : `int`
        The user's balance.
    
    required_balance : `int`
        Required balance for the role.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed_self(role, balance, required_balance)
    vampytest.assert_instance(output, Embed)
    return output
