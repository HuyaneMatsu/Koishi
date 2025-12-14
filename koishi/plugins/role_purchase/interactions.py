__all__ = ()

from hata import DiscordException, ERROR_CODES, create_text_display

from ...bot_utils.constants import EMOJI__HEART_CURRENCY
from ...bot_utils.user_getter import get_user
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS, MAIN_CLIENT

from ..gift_common import can_gift, produce_gift_requirements_unsatisfied_error_message
from ..relationships_core import deepen_and_boost_relationship, get_relationship_to_deepen
from ..user_balance import get_user_balance
from ..user_settings import get_one_user_settings, get_preferred_client_for_user

from .constants import PURCHASABLE_ROLES
from .content_building import (
    produce_buy_role_success_description, produce_buy_role_notification_description
)
from .custom_ids import CUSTOM_ID_BUY_ROLE_CONFIRMATION_RP


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_BUY_ROLE_CONFIRMATION_RP, target = 'form')
async def handle_buy_role_confirmation(
    client,
    interaction_event,
    role_id,
    target_user_id,
):
    """
    Handles a buy role confirmation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    role_id : `str`
        The purchased role's identifier as a hexadecimal integer.
    
    target_user_id : `str`
        The targeted user's identifier as hexadecimal integer.
    """
    try:
        role_id = int(role_id, 16)
        target_user_id = int(target_user_id, 16)
    except ValueError:
        return
    
    try:
        role, required_balance = PURCHASABLE_ROLES[role_id]
    except KeyError:
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
        current_balance = source_user_balance.balance
        available_balance = current_balance - source_user_balance.get_cumulative_allocated_balance()
        
        if available_balance < required_balance:
            error_message = (
                f'You have only {available_balance!s} available {EMOJI__HEART_CURRENCY}, '
                f'which is lower than the required {required_balance!s}.'
            )
            break
        
        try:
            await MAIN_CLIENT.user_role_add((interaction_event.user if target_user is None else target_user), role)
        except DiscordException as err:
            if err.code in (
                ERROR_CODES.unknown_user,
                ERROR_CODES.unknown_member,
            ):
                success = False
            
            else:
                raise
        
        else:
            success = True
        
        if not success:
            error_message = f'Failed to purchase {role.name} role.'
            break
        
        if target_user is None:
            target_user_balance = None
        else:
            target_user_balance = await get_user_balance(target_user.id)
        
        source_user_balance.modify_balance_by(-required_balance)
        
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
            content = ''.join([*produce_buy_role_success_description(
                role,
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
                            ''.join(''.join([*produce_buy_role_notification_description(
                                role, interaction_event.user, interaction_event.guild_id
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
        )
