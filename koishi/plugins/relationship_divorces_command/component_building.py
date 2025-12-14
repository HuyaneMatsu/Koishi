__all__ = ()

from hata import InteractionForm, create_text_display

from .content_building import produce_burn_divorce_papers_confirmation_description
from .custom_ids import CUSTOM_ID_BURN_DIVORCE_PAPERS_CONFIRMATION_BUILDER


def build_confirmation_form(
    relationship_divorces,
    required_balance,
    target_user,
    guild_id,
):
    """
    Builds a burn divorce papers confirmation form.
    
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
    interaction_form : ``InteractionForm``
    """
    return InteractionForm(
        'Confirm hiring ninjas',
        [
            create_text_display(
                ''.join([*produce_burn_divorce_papers_confirmation_description(
                    relationship_divorces,
                    required_balance,
                    target_user,
                    guild_id,
                )])
            ),
        ],
        CUSTOM_ID_BURN_DIVORCE_PAPERS_CONFIRMATION_BUILDER(
            (0 if target_user is None else target_user.id),
        ),
    )
