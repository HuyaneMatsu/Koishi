import vampytest
from hata import Embed, Role

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_failure_embed_insufficient_available_balance


def _iter_options():
    role_id = 202502130013
    guild_id = 202502130014
    
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    
    yield (
        role,
        2000,
        3000,
        Embed(
            'Insufficient available balance',
            (
                f'You need to have at least 3000 available {EMOJI__HEART_CURRENCY} '
                f'to purchase the Nyan role.'
            )
        ).add_field(
            f'Your available {EMOJI__HEART_CURRENCY}',
            (
                f'```\n'
                f'2000\n'
                f'```'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_insufficient_available_balance(role, available_balance, required_balance):
    """
    Tests whether ``build_failure_embed_insufficient_available_balance`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The role to check for.
    
    available_balance : `int`
        Available balance.
    
    required_balance : `int`
        The required balance to buy the role.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_insufficient_available_balance(role, available_balance, required_balance)
    vampytest.assert_instance(output, Embed)
    return output
