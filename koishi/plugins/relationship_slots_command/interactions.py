__all__ = ()

from hata import InteractionType, create_text_display

from ...bot_utils.constants import EMOJI__HEART_CURRENCY, MAX_WAIFU_SLOTS, WAIFU_SLOT_COSTS, WAIFU_SLOT_COST_DEFAULT
from ...bot_utils.user_getter import get_user
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..gift_common import can_gift, produce_gift_requirements_unsatisfied_error_message
from ..relationship_slots_core import CUSTOM_ID_BUY_RELATIONSHIP_SLOT_INVOKE_RP
from ..relationships_core import deepen_and_boost_relationship, get_relationship_to_deepen
from ..user_balance import get_user_balance
from ..user_settings import (
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_GIFT, get_one_user_settings, get_preferred_client_for_user
)

from .component_building import build_confirmation_form
from .content_building import (
    produce_buy_relationship_slot_success_description, produce_buy_relationship_slot_notification_description
)
from .custom_ids import CUSTOM_ID_BUY_RELATIONSHIP_SLOT_CONFIRMATION_RP


async def relationship_increment_respond(client, interaction_event, target_user, relationship_to_deepen):
    """
    Responds the user whether the relationship slot count should be incremented.
    
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
            relationship_slots = source_user_balance.relationship_slots
        else:
            target_user_balance = await get_user_balance(target_user.id)
            relationship_slots = target_user_balance.relationship_slots
        
        if relationship_slots >= MAX_WAIFU_SLOTS:
            error_message = (
                f'{"You" if target_user is None else target_user.name_at(interaction_event.guild_id)} '
                f'reached their maximum amount of relationship slots.'
            )
            break
        
        new_relationship_slot_count = relationship_slots + 1
        required_balance = WAIFU_SLOT_COSTS.get(new_relationship_slot_count, WAIFU_SLOT_COST_DEFAULT)
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
                new_relationship_slot_count,
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


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_BUY_RELATIONSHIP_SLOT_INVOKE_RP)
async def handle_buy_relationship_slot_invocation(
    client,
    interaction_event,
    target_user_id,
):
    """
    Handles a buy relationship slot invocation.
    
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
    
    await relationship_increment_respond(client, interaction_event, target_user, relationship_to_deepen)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_BUY_RELATIONSHIP_SLOT_CONFIRMATION_RP, target = 'form')
async def handle_buy_relationship_slot_confirmation(
    client,
    interaction_event,
    target_user_id,
):
    """
    Handles a buy relationship slot confirmation.
    
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
    
    if interaction_event.type is InteractionType.application_command:
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
            relationship_slots = source_user_balance.relationship_slots
        else:
            target_user_balance = await get_user_balance(target_user.id)
            relationship_slots = target_user_balance.relationship_slots
        
        if relationship_slots >= MAX_WAIFU_SLOTS:
            error_message = (
                f'{"You" if target_user is None else target_user.name_at(interaction_event.guild_id)} '
                f'reached their maximum amount of relationship slots.'
            )
            break
        
        new_relationship_slot_count = relationship_slots + 1
        required_balance = WAIFU_SLOT_COSTS.get(new_relationship_slot_count, WAIFU_SLOT_COST_DEFAULT)
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
            source_user_balance.increment_relationship_slots()
        else:
            target_user_balance.increment_relationship_slots()
        
        await deepen_and_boost_relationship(
            source_user_balance,
            target_user_balance,
            relationship_to_deepen,
            required_balance,
            save_source_user_balance = 2,
            save_target_user_balance = 2,
        )
        
        if interaction_event.type is InteractionType.application_command:
            await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
            await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            content = ''.join([*produce_buy_relationship_slot_success_description(
                new_relationship_slot_count,
                current_balance,
                required_balance,
                target_user,
                interaction_event.guild_id,
            )]),
        )
        
        if (target_user is not None) and (not target_user.bot):
            target_user_settings = await get_one_user_settings(target_user.id)
            if (target_user_settings.notification_flags >> USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_GIFT) & 1:
                await send_embed_to(
                    get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                    target_user,
                    None,
                    [
                        create_text_display(
                            ''.join(''.join([*produce_buy_relationship_slot_notification_description(
                                new_relationship_slot_count, interaction_event.user, interaction_event.guild_id
                            )]))
                        ),
                    ],
                )
        
        return
    
    
    if interaction_event.type is InteractionType.application_command:
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
