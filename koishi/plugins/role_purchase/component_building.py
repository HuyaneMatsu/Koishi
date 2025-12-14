__all__ = ()

from hata import InteractionForm, create_text_display

from .content_building import produce_buy_role_confirmation_description
from .custom_ids import CUSTOM_ID_BUY_ROLE_CONFIRMATION_BUILDER


def build_confirmation_form(
    role,
    required_balance,
    target_user,
    guild_id,
):
    """
    Builds buy role confirmation form.
    
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
    interaction_form : ``InteractionForm``
    """
    return InteractionForm(
        'Confirm buying role',
        [
            create_text_display(
                ''.join([*produce_buy_role_confirmation_description(
                    role,
                    required_balance,
                    target_user,
                    guild_id,
                )])
            ),
        ],
        CUSTOM_ID_BUY_ROLE_CONFIRMATION_BUILDER(
            role.id, (0 if target_user is None else target_user.id),
        ),
    )
