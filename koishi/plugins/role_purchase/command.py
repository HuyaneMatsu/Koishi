__all__ = ('command_buy_role',)

from hata import ClientUserBase
from hata.ext.slash import P

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..gift_common import can_gift, identify_targeted_user, produce_gift_requirements_unsatisfied_error_message
from ..relationships_core import autocomplete_relationship_extended_user_name
from ..user_balance import get_user_balance

from .component_building import build_confirmation_form
from .constants import PURCHASABLE_ROLES, ROLE_CHOICES


async def command_buy_role(
    client,
    interaction_event,
    role_id: P(ROLE_CHOICES, 'Choose a role to buy!', 'role'),
    target_related_name : P(
        str,
        'Buy role for someone related',
        'related',
        autocomplete = autocomplete_relationship_extended_user_name,
    ) = None,
    target_user : P(
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
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    role_id : `str
        The targeted role's identifier as hexadecimal integer.
    
    target_related_name : `None | str` = `None`, Optional
        The targeted related user's name.
    
    target_user : `None | ClientUserBase` = `None`, Optional
        The targeted user.
    """
    try:
        role_id = int(role_id, 16)
    except ValueError:
        return
    
    try:
        role, required_balance = PURCHASABLE_ROLES[role_id]
    except KeyError:
        return
    
    while True:
        target_user_and_relationship_to_deepen = await identify_targeted_user(
            interaction_event.user, target_related_name, target_user, interaction_event.guild_id
        )
        if (target_user_and_relationship_to_deepen is None):
            error_message = 'Could not match anyone.'
            break
        
        target_user, relationship_to_deepen = target_user_and_relationship_to_deepen
        
        if (target_user is not None) and (not can_gift(interaction_event.user, relationship_to_deepen)):
            error_message = ''.join([*produce_gift_requirements_unsatisfied_error_message()])
            break
        
        
        if role.guild_id not in (interaction_event.user if target_user is None else target_user).guild_profiles:
            error_message = (
                f'{"You" if target_user is None else target_user.name_at(interaction_event.guild_id)} '
                f'{"have" if target_user is None else "has"} to be in my support guild to buy {role.name} role.'
            )
            break
            
        if (interaction_event.user if target_user is None else target_user).has_role(role):
            error_message = (
                f'{"You" if target_user is None else target_user.name_at(interaction_event.guild_id)} '
                f'already {"have" if target_user is None else "has"} {role.name} role.'
            )
            break
        
        
        source_user_balance = await get_user_balance(interaction_event.user_id)
        available_balance = source_user_balance.balance - source_user_balance.get_cumulative_allocated_balance()
        
        if available_balance < required_balance:
            error_message = (
                f'You have only {available_balance!s} available {EMOJI__HEART_CURRENCY}, '
                f'which is lower than the required {required_balance!s}.'
            )
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_confirmation_form(
                role,
                required_balance,
                target_user,
                interaction_event.guild_id,
            ),
        )
        return
    
    
    await client.interaction_response_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )
    return
