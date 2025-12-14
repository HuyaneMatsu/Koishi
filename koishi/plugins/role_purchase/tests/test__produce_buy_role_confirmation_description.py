import vampytest
from hata import User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY, ROLE__SUPPORT__ELEVATED

from ..content_building import produce_buy_role_confirmation_description


def _iter_options():
    user = User.precreate(
        202512030021,
        name = 'Satori',
    )
    
    yield (
        ROLE__SUPPORT__ELEVATED,
        6000,
        None,
        0,
        (
            f'Are you sure to buy {ROLE__SUPPORT__ELEVATED.name} role?\n'
            f'\n'
            f'It will cost you 6000 {EMOJI__HEART_CURRENCY}.'
        ),
    )
    yield (
        ROLE__SUPPORT__ELEVATED,
        6000,
        user,
        0,
        (
            f'Are you sure to buy {ROLE__SUPPORT__ELEVATED.name} role for Satori?\n'
            f'\n'
            f'It will cost you 6000 {EMOJI__HEART_CURRENCY}.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_buy_role_confirmation_description(
    role,
    required_balance,
    target_user,
    guild_id,
):
    """
    Tests whether ``produce_buy_role_confirmation_description`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
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
    output = [*produce_buy_role_confirmation_description(
        role,
        required_balance,
        target_user,
        guild_id,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
