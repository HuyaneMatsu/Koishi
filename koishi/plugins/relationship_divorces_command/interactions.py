__all__ = ()

from hata import InteractionType, create_text_display

from ...bot_utils.constants import EMOJI__HEART_CURRENCY
from ...bot_utils.user_getter import get_user
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..gift_common import can_gift, produce_gift_requirements_unsatisfied_error_message
from ..relationships_core import deepen_and_boost_relationship, get_relationship_to_deepen
from ..relationship_divorces_core import CUSTOM_ID_BURN_DIVORCE_PAPERS_INVOKE_RP
from ..user_balance import get_user_balance
from ..user_settings import get_one_user_settings, get_preferred_client_for_user

from .component_building import build_confirmation_form
from .content_building import (
    produce_burn_divorce_papers_success_description, produce_burn_divorce_papers_notification_description
)
from .custom_ids import CUSTOM_ID_BURN_DIVORCE_PAPERS_CONFIRMATION_RP
from .helpers import get_relationship_divorce_reduction_required_balance


async def burn_divorce_papers_respond(client, interaction_event, target_user, relationship_to_deepen):
    """
    Responds the user whether the it wants to burn its divorce papers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``None | ClientUserBase``
        The targeted user.
    
    relationship_to_deepen : ``None | Relationship``
        The relationship to deepen by the purchase.
    """
    while True:
        if (target_user is not None) and (not can_gift(interaction_event.user, relationship_to_deepen)):
            error_message = ''.join([*produce_gift_requirements_unsatisfied_error_message()])
            break
        
        source_user_balance = await get_user_balance(interaction_event.user_id)
        
        if target_user is None:
            relationship_divorces = source_user_balance.relationship_divorces
        else:
            target_user_balance = await get_user_balance(target_user.id)
            relationship_divorces = target_user_balance.relationship_divorces
        
        if not relationship_divorces:
            error_message = (
                f'{"You" if target_user is None else target_user.name_at(interaction_event.guild_id)} '
                f'{"have" if target_user is None else "has"} no divorces.'
            )
            break
        
        required_balance = get_relationship_divorce_reduction_required_balance(
            (interaction_event.user_id if target_user is None else target_user.id),
            relationship_divorces,
        )
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
                relationship_divorces,
                required_balance,
                target_user,
                interaction_event.guild_id,
            ),
        )
        return
    
    
    if interaction_event.type is InteractionType.application_command:
        await client.interaction_response_message_create(
            interaction_event,
            content = error_message,
            show_for_invoking_user_only = True,
        )
    
    else:
        await client.interaction_component_acknowledge(interaction_event)
        await client.interaction_followup_message_create(
            interaction_event,
            content = error_message,
            show_for_invoking_user_only = True,
        )
    return


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_BURN_DIVORCE_PAPERS_INVOKE_RP)
async def handle_burn_divorce_papers_invocation(
    client,
    interaction_event,
    target_user_id,
):
    """
    Handles a burn divorce papers interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user_id : `str`
        The targeted user's identifier as hexadecimal integer.
    """
    try:
        target_user_id = int(target_user_id, 16)
    except ValueError:
        return
    
    if target_user_id:
        target_user = await get_user(target_user_id)
        relationship_to_deepen = await get_relationship_to_deepen(interaction_event.user_id, target_user_id)
    else:
        target_user = None
        relationship_to_deepen = None
    
    await burn_divorce_papers_respond(client, interaction_event, target_user, relationship_to_deepen)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_BURN_DIVORCE_PAPERS_CONFIRMATION_RP, target = 'form')
async def handle_burn_divorce_papers_confirmation(
    client,
    interaction_event,
    target_user_id,
):
    """
    Handles a burn divorce papers confirmation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user_id : `str`
        The targeted user's identifier as hexadecimal integer.
    """
    try:
        target_user_id = int(target_user_id, 16)
    except ValueError:
        return
    
    invoked_through_application_command = (interaction_event.message is None)
    
    if invoked_through_application_command:
        await client.interaction_application_command_acknowledge(
            interaction_event,
            False,
            show_for_invoking_user_only = True,
        )
    else:
        await client.interaction_component_acknowledge(
            interaction_event,
            False,
        )
    
    while True:
        if target_user_id:
            target_user = await get_user(target_user_id)
            relationship_to_deepen = await get_relationship_to_deepen(interaction_event.user_id, target_user_id)
        else:
            target_user = None
            relationship_to_deepen = None
        
        if (target_user is not None) and (not can_gift(interaction_event.user, relationship_to_deepen)):
            error_message = ''.join([*produce_gift_requirements_unsatisfied_error_message()])
            break
        
        
        source_user_balance = await get_user_balance(interaction_event.user_id)
        
        if target_user is None:
            target_user_balance = None
            relationship_divorces = source_user_balance.relationship_divorces
        else:
            target_user_balance = await get_user_balance(target_user.id)
            relationship_divorces = target_user_balance.relationship_divorces
        
        if not relationship_divorces:
            error_message = (
                f'{"You" if target_user is None else target_user.name_at(interaction_event.guild_id)} '
                f'{"have" if target_user is None else "has"} no divorces.'
            )
            break
        
        required_balance = get_relationship_divorce_reduction_required_balance(
            (target_user_id if target_user_id else interaction_event.user_id),
            relationship_divorces,
        )
        current_balance = source_user_balance.balance
        available_balance = current_balance - source_user_balance.get_cumulative_allocated_balance()
        
        if available_balance < required_balance:
            error_message = (
                f'You have only {available_balance!s} available {EMOJI__HEART_CURRENCY}, '
                f'which is lower than the required {required_balance!s}.'
            )
            break
        
        source_user_balance.modify_balance_by(-required_balance)
        if target_user_balance is None:
            source_user_balance.decrement_relationship_divorces()
        else:
            target_user_balance.decrement_relationship_divorces()
        
        await deepen_and_boost_relationship(
            source_user_balance,
            target_user_balance,
            relationship_to_deepen,
            required_balance,
            save_source_user_balance = 2,
            save_target_user_balance = 2,
        )
        
        if invoked_through_application_command:
            await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
            await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            content = ''.join([*produce_burn_divorce_papers_success_description(
                relationship_divorces,
                current_balance,
                required_balance,
                target_user,
                interaction_event.guild_id,
            )]),
        )
        
        if (target_user is not None) and (not target_user.bot):
            target_user_settings = await get_one_user_settings(target_user.id)
            if target_user_settings.notification_gift:
                await send_embed_to(
                    get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                    target_user,
                    None,
                    [
                        create_text_display(
                            ''.join(''.join([*produce_burn_divorce_papers_notification_description(
                                relationship_divorces, interaction_event.user, interaction_event.guild_id
                            )]))
                        ),
                    ],
                )
        
        return
    
    
    if invoked_through_application_command:
        await client.interaction_response_message_edit(
            interaction_event,
            content = error_message,
        )
    else:
        await client.interaction_followup_message_create(
            interaction_event,
            content = error_message,
            show_for_invoking_user_only = True,
        )
