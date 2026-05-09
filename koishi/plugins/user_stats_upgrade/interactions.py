__all__ = ()

from hata import create_text_display

from ...bot_utils.constants import EMOJI__HEART_CURRENCY
from ...bot_utils.user_getter import get_user
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..gift_common import can_gift, produce_gift_requirements_unsatisfied_error_message
from ..relationships_core import deepen_and_boost_relationship, get_relationship_to_deepen
from ..user_balance import get_user_balance
from ..user_settings import (
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_GIFT, get_one_user_settings, get_preferred_client_for_user
)
from ..user_stats_core import get_user_stats, save_user_stats

from .content_building import produce_stat_upgrade_success_description, produce_stat_upgraded_notification_description
from .custom_ids import CUSTOM_ID_UPGRADE_STATS_CONFIRMATION_RP
from .helpers import get_upgrade_cost_cumulative


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_UPGRADE_STATS_CONFIRMATION_RP, target = 'form')
async def handle_stat_upgrade_confirmation(
    client,
    interaction_event,
    modify_housewife_by,
    modify_cuteness_by,
    modify_bedroom_by,
    modify_charm_by,
    modify_loyalty_by,
    target_user_id,
):
    """
    Handles a stat upgrade confirmation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    modify_housewife_by : `str`
        The amount to modify the housewife stat by as hexadecimal integer.
    
    modify_cuteness_by : `str`
        The amount to modify the cuteness stat by as hexadecimal integer.
    
    modify_bedroom_by : `str`
        The amount to modify the bedroom stat by as hexadecimal integer.
    
    modify_charm_by : `str`
        The amount to modify the charm stat by as hexadecimal integer.
    
    modify_loyalty_by : `str`
        The amount to modify the loyalty stat by as hexadecimal integer.
    
    target_user_id : `str`
        The target user's identifier as hexadecimal integer.
    """
    try:
        modify_housewife_by = int(modify_housewife_by, 16)
        modify_cuteness_by = int(modify_cuteness_by, 16)
        modify_bedroom_by = int(modify_bedroom_by, 16)
        modify_charm_by = int(modify_charm_by, 16)
        modify_loyalty_by = int(modify_loyalty_by, 16)
        target_user_id = int(target_user_id, 16)
    except ValueError:
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
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
        
        user_stats = await get_user_stats(interaction_event.user_id if (target_user is None) else target_user.id)
        
        stat_housewife = user_stats.stat_housewife
        stat_cuteness = user_stats.stat_cuteness
        stat_bedroom = user_stats.stat_bedroom
        stat_charm = user_stats.stat_charm
        stat_loyalty = user_stats.stat_loyalty
    
        required_balance = get_upgrade_cost_cumulative(
            stat_housewife,
            stat_cuteness,
            stat_bedroom,
            stat_charm,
            stat_loyalty,
            modify_housewife_by,
            modify_cuteness_by,
            modify_bedroom_by,
            modify_charm_by,
            modify_loyalty_by,
        )
        
        source_user_balance = await get_user_balance(interaction_event.user_id)
        current_balance = source_user_balance.balance
        available_balance = current_balance - source_user_balance.get_cumulative_allocated_balance()
        
        if available_balance < required_balance:
            error_message = (
                f'You have only {available_balance!s} available {EMOJI__HEART_CURRENCY}, '
                f'which is lower than the required {required_balance!s}.'
            )
            break
        
        # Modify stats
        if modify_housewife_by:
            user_stats.modify_stat_housewife_by(modify_housewife_by)
        
        if modify_cuteness_by:
            user_stats.modify_stat_cuteness_by(modify_cuteness_by)
        
        if modify_bedroom_by:
            user_stats.modify_stat_bedroom_by(modify_bedroom_by)
        
        if modify_charm_by:
            user_stats.modify_stat_charm_by(modify_charm_by)
        
        if modify_loyalty_by:
            user_stats.modify_stat_loyalty_by(modify_loyalty_by)
        
        await save_user_stats(user_stats)
        
        # Apply payment
        source_user_balance.modify_balance_by(-required_balance)
        
        # Deepen
        if target_user_id:
            target_user_balance = await get_user_balance(target_user_id)
        else:
            target_user_balance = None
        
        await deepen_and_boost_relationship(
            source_user_balance,
            target_user_balance,
            relationship_to_deepen,
            required_balance,
            save_source_user_balance = 2,
            save_target_user_balance = 2,
        )
        
        
        # Respond
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            content = ''.join([*produce_stat_upgrade_success_description(
                stat_housewife,
                stat_cuteness,
                stat_bedroom,
                stat_charm,
                stat_loyalty,
                modify_housewife_by,
                modify_cuteness_by,
                modify_bedroom_by,
                modify_charm_by,
                modify_loyalty_by,
                current_balance,
                required_balance,
                target_user,
                interaction_event.guild_id,
            )]),
            allowed_mentions = None,
        )
        
        # Notify
        if (target_user is not None) and (not target_user.bot):
            target_user_settings = await get_one_user_settings(target_user.id)
            if (target_user_settings.notification_flags >> USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_GIFT) & 1:
                await send_embed_to(
                    get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                    target_user,
                    None,
                    [
                        create_text_display(''.join([*produce_stat_upgraded_notification_description(
                            stat_housewife,
                            stat_cuteness,
                            stat_bedroom,
                            stat_charm,
                            stat_loyalty,
                            modify_housewife_by,
                            modify_cuteness_by,
                            modify_bedroom_by,
                            modify_charm_by,
                            modify_loyalty_by,
                            interaction_event.user,
                            interaction_event.guild_id,
                        )])),
                    ],
                )
        
        return
    
    await client.interaction_followup_message_edit(
        interaction_event,
        content = error_message,
    )
