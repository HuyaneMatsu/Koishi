import vampytest
from hata import InteractionForm, User, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..component_building import build_confirmation_form


def _iter_options():
    user = User.precreate(
        202512020000,
        name = 'Satori',
    )
    
    yield (
        5,
        6000,
        None,
        0,
        InteractionForm(
            'Confirm hiring ninjas',
            [
                create_text_display(
                    f'Are you sure to hire ninjas to locate and burn your 5th divorce papers?\n'
                    f'\n'
                    f'It will cost you 6000 {EMOJI__HEART_CURRENCY}.'
                ),
            ],
            'user.burn_divorce_papers.0',
        ),
    )
    
    yield (
        5,
        6000,
        user,
        0,
        InteractionForm(
            'Confirm hiring ninjas',
            [
                create_text_display(
                    f'Are you sure to hire ninjas to locate and burn Satori\'s 5th divorce papers?\n'
                    f'\n'
                    f'It will cost you 6000 {EMOJI__HEART_CURRENCY}.'
                ),
            ],
            f'user.burn_divorce_papers.{user.id:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_confirmation_form(
    relationship_divorces,
    required_balance,
    target_user,
    guild_id,
):
    """
    Tests whether ``build_confirmation_form`` works as intended.
    
    Parameters
    ----------
    relationship_divorces : `int`
        The amount of divorces the user has.
    
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
        relationship_divorces,
        required_balance,
        target_user,
        guild_id,
    )
    vampytest.assert_instance(output, InteractionForm)
    return output
