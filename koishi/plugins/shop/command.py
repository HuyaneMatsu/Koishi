__all__ = ()

from hata import ClientUserBase
from hata.ext.slash import P

from ...bots import FEATURE_CLIENTS

from ..relationship_divorces_interactions import (
    relationship_divorces_decrement_invoke_other_question, relationship_divorces_decrement_invoke_self_question
)
from ..relationship_slots_interactions import (
    relationship_slot_increment_invoke_other_question, relationship_slot_increment_invoke_self_question
)
from ..relationships_core import (
    autocomplete_relationship_extended_user_name, get_extender_relationship_and_relationship_and_user_like_at
)
from ..role_purchase import PURCHASABLE_ROLES, ROLE_CHOICES, purchase_role_other, purchase_role_self


SHOP = FEATURE_CLIENTS.interactions(
    None,
    name = 'shop',
    description = 'Trade your hearts!',
    is_global = True,
)


@SHOP.interactions
async def buy_relationship_slot(
    event,
    target_related_name : P(
        str,
        'Buy relationship slot for someone related',
        'related',
        autocomplete = autocomplete_relationship_extended_user_name,
    ) = None,
    target_user : (
        ClientUserBase,
        'Buy waifu slot for someone else?',
        'someone-else',
    ) = None,
):
    """
    Buy relationship slots to increase your family's size <3.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    role_choice : `str`
        The chosen role.
    
    target_related_name : `None | str` = `None`, Optional
        The targeted related user's name.
    
    target_user : `None | ClientUserBase` = `None`, Optional
        The targeted user.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if (target_user is None) and (target_related_name is not None):
        extender_relationship, relationship, target_user = (
            await get_extender_relationship_and_relationship_and_user_like_at(
                event.user_id, target_related_name, event.guild_id
            )
        )
    
    if (target_user is None) or (target_user is event.user):
        coroutine = relationship_slot_increment_invoke_self_question(event)
    else:
        coroutine = relationship_slot_increment_invoke_other_question(event, target_user)
    
    return await coroutine


@SHOP.interactions
async def burn_divorce_papers(
    event,
    target_related_name : P(
        str,
        'Hire ninjas to burn and locate divorce papers for someone related',
        'related',
        autocomplete = autocomplete_relationship_extended_user_name,
    ) = None,
    target_user : (
        ClientUserBase,
        'Hire ninjas to burn an locate divorce papers for someone else?',
        'someone-else',
    ) = None,
):
    """
    Burn divorce papers stockpiled on breakups.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    role_choice : `str`
        The chosen role.
    
    target_related_name : `None | str` = `None`, Optional
        The targeted related user's name.
    
    target_user : `None | ClientUserBase` = `None`, Optional
        The targeted user.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if (target_user is None) and (target_related_name is not None):
        extender_relationship, relationship, target_user = (
            await get_extender_relationship_and_relationship_and_user_like_at(
                event.user_id, target_related_name, event.guild_id
            )
        )
    
    if (target_user is None) or (target_user is event.user):
        coroutine = relationship_divorces_decrement_invoke_self_question(event)
    else:
        coroutine = relationship_divorces_decrement_invoke_other_question(event, target_user)
    
    return await coroutine


@SHOP.interactions
async def roles(
    client,
    event,
    role_choice: (ROLE_CHOICES, 'Choose a role to buy!', 'role'),
    target_related_name : P(
        str,
        'Buy role for someone related',
        'related',
        autocomplete = autocomplete_relationship_extended_user_name,
    ) = None,
    target_user : (
        ClientUserBase,
        'Buy role slot for someone else?',
        'someone-else',
    ) = None,
):
    """
    Buy roles to enhance your love!
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    role_choice : `str`
        The chosen role.
    
    target_related_name : `None | str` = `None`, Optional
        The targeted related user's name.
    
    target_user : `None | ClientUserBase` = `None`, Optional
        The targeted user.
    """
    role, required_balance = PURCHASABLE_ROLES[role_choice]
    
    if (target_user is None) and (target_related_name is not None):
        extender_relationship, relationship, target_user = (
            await get_extender_relationship_and_relationship_and_user_like_at(
                event.user_id, target_related_name, event.guild_id
            )
        )
    
    if (target_user is None) or (target_user is event.user):
        coroutine = purchase_role_self(client, event, role, required_balance)
    else:
        coroutine = purchase_role_other(client, event, role, required_balance, target_user)
    
    return await coroutine
