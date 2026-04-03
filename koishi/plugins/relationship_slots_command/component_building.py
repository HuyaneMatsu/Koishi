__all__ = ()

from hata import InteractionForm, create_text_display

from .content_building import produce_buy_relationship_slot_confirmation_description
from .custom_ids import CUSTOM_ID_BUY_RELATIONSHIP_SLOT_CONFIRMATION_BUILDER


def build_confirmation_form(
    new_relationship_slot_count,
    required_balance,
    target_user,
    guild_id,
):
    """
    Builds buy relationship slot confirmation form.
    
    Parameters
    ----------
    new_relationship_slot_count : `int`
        The relationship slot count after purchase.
    
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
        'Confirm buying relationship slot',
        [
            create_text_display(
                ''.join([*produce_buy_relationship_slot_confirmation_description(
                    new_relationship_slot_count,
                    required_balance,
                    target_user,
                    guild_id,
                )])
            ),
        ],
        CUSTOM_ID_BUY_RELATIONSHIP_SLOT_CONFIRMATION_BUILDER(
            (0 if target_user is None else target_user.id),
        ),
    )
