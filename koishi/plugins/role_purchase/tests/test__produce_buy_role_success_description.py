import vampytest
from hata import User


from ....bot_utils.constants import EMOJI__HEART_CURRENCY, ROLE__SUPPORT__ELEVATED

from ..content_building import produce_buy_role_success_description


def _iter_options():
    user = User.precreate(
        2025120300203,
        name = 'Satori',
    )
    
    yield (
        ROLE__SUPPORT__ELEVATED,
        7000,
        6000,
        None,
        0,
        (
            f'You purchased {ROLE__SUPPORT__ELEVATED.name} role.\n'
            f'\n'
            f'Your {EMOJI__HEART_CURRENCY}:\n'
            f'```ansi\n'
            f'7000 \x1b[31m->\x1b[0m 1000\n'
            f'```'
        ),
    )
    
    yield (
        ROLE__SUPPORT__ELEVATED,
        7000,
        6000,
        user,
        0,
        (
            f'You purchased {ROLE__SUPPORT__ELEVATED.name} role for Satori.\n'
            f'\n'
            f'Your {EMOJI__HEART_CURRENCY}:\n'
            f'```ansi\n'
            f'7000 \x1b[31m->\x1b[0m 1000\n'
            f'```'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_buy_role_success_description(
    new_role_count,
    current_balance,
    required_balance,
    target_user,
    guild_id,
):
    """
    Tests whether ``produce_buy_role_success_description`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    current_balance : `int`
        The user's current balance.
    
    required_balance : `int`
        The required balance for upgrading.
    
    target_user : ``None | ClientUserBase``
        The targeted user if any.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_buy_role_success_description(
        new_role_count,
        current_balance,
        required_balance,
        target_user,
        guild_id,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
