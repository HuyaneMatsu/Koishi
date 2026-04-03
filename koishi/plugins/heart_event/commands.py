__all__ = ()

from hata import Permission, parse_tdelta

from ...bot_utils.constants import GUILD__SUPPORT
from ...bots import FEATURE_CLIENTS

from .constants import (
    EVENT_DAILY_MAX_AMOUNT, EVENT_DAILY_MIN_AMOUNT, EVENT_HEART_MAX_AMOUNT, EVENT_HEART_MIN_AMOUNT,
    EVENT_MAX_DURATION, EVENT_MIN_DURATION, EVENT_MODE_STREAK, EVENT_MODE_HEART
)
from .helpers import convert_time_delta
from .component_building import build_event_confirmation_form


@FEATURE_CLIENTS.interactions(
    guild = GUILD__SUPPORT,
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def heart_event(
    client,
    interaction_event,
    duration : ('str', 'The event\'s duration.'),
    amount : ('int', 'The hearst to earn.'),
    user_limit : ('int', 'The maximal amount fo claimers.') = 0,
):
    """
    Starts a heart event at the channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    duration : `str`
        String representing the event's duration.
    
    amount : `int`
        Amount of hearts to give.
    
    user_limit : `int`
        The maximal amount of users allowed to receive reward.
    """
    while True:
        if not interaction_event.user_permissions.administrator:
            error_message = 'You must be administrator to invoke this command..'
            break
        
        guild = interaction_event.guild
        if (guild is not None):
            if (client.get_guild_profile_for(guild) is None):
                error_message = 'Please add me to the guild before invoking the command.'
                break
        
        duration = parse_tdelta(duration)
        if (duration is None):
            error_message = 'Could not interpret the given duration.'
            break
        
        if duration > EVENT_MAX_DURATION:
            error_message = (
                f'**Duration passed the upper limit**\n'
                f'**>** upper limit : {convert_time_delta(EVENT_MAX_DURATION)}\n'
                f'**>** passed : {convert_time_delta(duration)}'
            )
            break
        
        if duration < EVENT_MIN_DURATION:
            error_message = (
                f'**Duration passed the lower limit**\n'
                f'**>** lower limit : {convert_time_delta(EVENT_MIN_DURATION)}\n'
                f'**>** passed : {convert_time_delta(duration)}'
            )
            break
        
        if amount > EVENT_HEART_MAX_AMOUNT:
            error_message = (
                f'**Amount passed the upper limit**\n'
                f'**>** upper limit : {EVENT_HEART_MAX_AMOUNT}\n'
                f'**>** passed : {amount}'
            )
            break
        
        if amount < EVENT_HEART_MIN_AMOUNT:
            error_message = (
                f'**Amount passed the lower limit**\n'
                f'**>** lower limit : {EVENT_HEART_MIN_AMOUNT}\n'
                f'**>** passed : {amount}'
            )
            break
        
        if user_limit < 0:
            error_message = (
                f'**User limit passed the lower limit**\n'
                f'**>** lower limit : 0\n'
                f'**>** - passed : {user_limit}'
            )
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_event_confirmation_form(EVENT_MODE_HEART, duration, amount, user_limit),
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )
    return


@FEATURE_CLIENTS.interactions(
    guild = GUILD__SUPPORT,
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def streak_event(
    client,
    interaction_event,
    duration: ('str', 'The event\'s duration.'),
    amount: ('int', 'The extra steaks to earn.'),
    user_limit: ('int', 'The maximal amount fo claimers.') = 0,
):
    """
    Starts a streak event at the channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    duration : `str`
        String representing the event's duration.
    
    amount : `int`
        Amount of streak to give.
    
    user_limit : `int`
        The maximal amount of users allowed to receive reward.
    """
    while True:
        if not interaction_event.user_permissions.administrator:
            error_message = 'You must be administrator to invoke this command..'
            break
        
        guild = interaction_event.guild
        if (guild is not None):
            if (client.get_guild_profile_for(guild) is None):
                error_message = 'Please add me to the guild before invoking the command.'
                break
        
        duration = parse_tdelta(duration)
        if (duration is None):
            error_message = 'Could not interpret the given duration.'
            break
        
        if duration > EVENT_MAX_DURATION:
            error_message = (
                f'Duration passed the upper limit\n'
                f'**>** upper limit : {convert_time_delta(EVENT_MAX_DURATION)}\n'
                f'**>** passed : {convert_time_delta(duration)}'
            )
            break
        
        if duration < EVENT_MIN_DURATION:
            error_message = (
                f'Duration passed the lower limit\n'
                f'**>** lower limit : {convert_time_delta(EVENT_MIN_DURATION)}\n'
                f'**>** passed : {convert_time_delta(duration)}'
            )
            break
        
        if amount > EVENT_DAILY_MAX_AMOUNT:
            error_message = (
                f'Amount passed the upper limit\n'
                f'**>** upper limit : {EVENT_DAILY_MAX_AMOUNT}\n'
                f'**>** passed : {amount}'
            )
            break
        
        if amount < EVENT_DAILY_MIN_AMOUNT:
            error_message = (
                f'Amount passed the lower limit\n'
                f'**>** lower limit : {EVENT_DAILY_MIN_AMOUNT}\n'
                f'**>** passed : {amount}'
            )
            break
        
        if user_limit < 0:
            error_message = (
                f'User limit passed the lower limit\n'
                f'**>** lower limit : 0\n'
                f'**>** passed : {user_limit}'
            )
            break
        
        
        await client.interaction_form_send(
            interaction_event,
            build_event_confirmation_form(EVENT_MODE_STREAK, duration, amount, user_limit),
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )
    return
