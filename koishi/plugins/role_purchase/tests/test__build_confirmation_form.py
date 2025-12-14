import vampytest
from hata import InteractionForm, User, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY, ROLE__SUPPORT__ELEVATED

from ..component_building import build_confirmation_form


def _iter_options():
    user = User.precreate(
        202512030020,
        name = 'Satori',
    )
    
    yield (
        ROLE__SUPPORT__ELEVATED,
        6000,
        None,
        0,
        InteractionForm(
            'Confirm buying role',
            [
                create_text_display(
                    f'Are you sure to buy {ROLE__SUPPORT__ELEVATED.name} role?\n'
                    f'\n'
                    f'It will cost you 6000 {EMOJI__HEART_CURRENCY}.'
                ),
            ],
            f'user.buy_role.{ROLE__SUPPORT__ELEVATED.id:x}.0',
        ),
    )
    
    yield (
        ROLE__SUPPORT__ELEVATED,
        6000,
        user,
        0,
        InteractionForm(
            'Confirm buying role',
            [
                create_text_display(
                    f'Are you sure to buy {ROLE__SUPPORT__ELEVATED.name} role for Satori?\n'
                    f'\n'
                    f'It will cost you 6000 {EMOJI__HEART_CURRENCY}.'
                ),
            ],
            f'user.buy_role.{ROLE__SUPPORT__ELEVATED.id:x}.{user.id:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_confirmation_form(
    role,
    required_balance,
    target_user,
    guild_id,
):
    """
    Tests whether ``build_confirmation_form`` works as intended.
    
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
    output : ``InteractionForm``
    """
    output = build_confirmation_form(
        role,
        required_balance,
        target_user,
        guild_id,
    )
    vampytest.assert_instance(output, InteractionForm)
    return output
