__all__ = ('command_upgrade_stats', )

from hata import ClientUserBase
from hata.ext.slash import P

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..gift_common import can_gift, identify_targeted_user, produce_gift_requirements_unsatisfied_error_message
from ..relationships_core import autocomplete_relationship_extended_user_name
from ..user_balance import get_user_balance
from ..user_stats_core import (
    USER_STAT_NAME_FULL_BEDROOM, USER_STAT_NAME_FULL_CHARM, USER_STAT_NAME_FULL_CUTENESS, USER_STAT_NAME_FULL_HOUSEWIFE,
    USER_STAT_NAME_FULL_LOYALTY, get_user_stats
)

from .component_building import build_confirmation_form
from .constants import STAT_UPGRADE_MAX, STAT_UPGRADE_MIN
from .helpers import get_upgrade_cost_cumulative


async def command_upgrade_stats(
    client,
    interaction_event,
    modify_housewife_by : P(
        int,
        'Upgrade housewife capabilities by',
        USER_STAT_NAME_FULL_HOUSEWIFE,
        min_value = STAT_UPGRADE_MIN,
        max_value = STAT_UPGRADE_MAX,
    ) = 0,
    modify_cuteness_by : P(
        int,
        'Upgrade cuteness by',
        USER_STAT_NAME_FULL_CUTENESS,
        min_value = STAT_UPGRADE_MIN,
        max_value = STAT_UPGRADE_MAX,
    ) = 0,
    modify_bedroom_by : P(
        int,
        'Upgrade bedroom skills by',
        USER_STAT_NAME_FULL_BEDROOM,
        min_value = STAT_UPGRADE_MIN,
        max_value = STAT_UPGRADE_MAX,
    ) = 0,
    modify_charm_by : P(
        int,
        'Upgrade charm by',
        USER_STAT_NAME_FULL_CHARM,
        min_value = STAT_UPGRADE_MIN,
        max_value = STAT_UPGRADE_MAX,
    ) = 0,
    modify_loyalty_by : P(
        int,
        'Upgrade loyalty by',
        USER_STAT_NAME_FULL_LOYALTY,
        min_value = STAT_UPGRADE_MIN,
        max_value = STAT_UPGRADE_MAX,
    ) = 0,
    target_related_name : P(
        str,
        'Buy relationship slot for someone related',
        'related',
        autocomplete = autocomplete_relationship_extended_user_name,
    ) = None,
    target_user : P(
        ClientUserBase,
        'Buy waifu slot for someone else?',
        'someone-else',
    ) = None,
):
    """
    Upgrade your or the selected user's stats.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    modify_housewife_by : `int` = `0`, Optional
        The amount to modify the housewife stat by.
    
    modify_cuteness_by : `int` = `0`, Optional
        The amount to modify the cuteness stat by.
    
    modify_bedroom_by : `int` = `0`, Optional
        The amount to modify the bedroom stat by.
    
    modify_charm_by : `int` = `0`, Optional
        The amount to modify the charm stat by.
    
    modify_loyalty_by : `int` = `0`, Optional
        The amount to modify the loyalty stat by.
    
    target_related_name : `None | str` = `None`, Optional
        The targeted related user's name.
    
    target_user : `None | ClientUserBase` = `None`, Optional
        The targeted user.
    """
    while True:
        target_user, relationship_to_deepen = await identify_targeted_user(
            interaction_event.user, target_related_name, target_user, interaction_event.guild_id
        )
        if (target_user is not None) and (not can_gift(interaction_event.user, relationship_to_deepen)):
            error_message = ''.join([*produce_gift_requirements_unsatisfied_error_message()])
            break
        
        if (modify_housewife_by < STAT_UPGRADE_MIN) or (modify_housewife_by > STAT_UPGRADE_MAX):
            error_message = '`housewife-capabilities` out of the expected range.'
            break
        
        if (modify_cuteness_by < STAT_UPGRADE_MIN) or (modify_housewife_by > STAT_UPGRADE_MAX):
            error_message = '`cuteness` out of the expected range.'
            break
        
        if (modify_bedroom_by < STAT_UPGRADE_MIN) or (modify_bedroom_by > STAT_UPGRADE_MAX):
            error_message = '`bedroom-skills` out of the expected range.'
            break
        
        if (modify_charm_by < STAT_UPGRADE_MIN) or (modify_housewife_by > STAT_UPGRADE_MAX):
            error_message = '`charm` out of the expected range.'
            break
        
        if (modify_loyalty_by < STAT_UPGRADE_MIN) or (modify_housewife_by > STAT_UPGRADE_MAX):
            error_message = '`loyalty` out of the expected range.'
            break
        
        if 0 == modify_housewife_by == modify_cuteness_by == modify_bedroom_by == modify_charm_by == modify_loyalty_by:
            error_message = 'Nothing to upgrade.'
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
        
        user_balance = await get_user_balance(interaction_event.user_id)
        available_balance = user_balance.balance - user_balance.get_cumulative_allocated_balance()
        
        if available_balance < required_balance:
            error_message = (
                f'You have only {available_balance!s} available {EMOJI__HEART_CURRENCY}, '
                f'which is lower than the required {required_balance!s}.'
            )
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_confirmation_form(
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
                required_balance,
                target_user,
                interaction_event.guild_id,
            )
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )
