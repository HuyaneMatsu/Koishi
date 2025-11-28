__all__ = ()

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

from ...bot_utils.constants import EMOJI__HEART_CURRENCY
from ...bot_utils.daily import calculate_daily_new
from ...bots import FEATURE_CLIENTS

from ..user_balance import get_user_balance, save_user_balance

from .component_building import build_event_active_components
from .constants import EVENT_MODE_HEART, EVENT_MODE_STREAK, SESSIONS
from .custom_ids import CUSTOM_ID_EVENT_ACTIVE, CUSTOM_ID_EVENT_CONFIRMATION_PATTERN, CUSTOM_ID_EVENT_INACTIVE
from .logic import ensure_session, step_session
from .session import Session


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_EVENT_CONFIRMATION_PATTERN, target = 'form')
async def handle_event_creation(
    client,
    interaction_event,
    event_mode,
    duration,
    amount,
    user_limit,
):
    """
    Handles event creation confirmation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    event_mode : `int`
        the event's mode as hexadecimal string
    
    duration : `int`
        Event duration as hexadecimal string
    
    amount : `int`
        Reward amount as hexadecimal string.
    
    user_limit : `int`
        The maximal amount of users allowed to receive reward as hexadecimal string.
    """
    try:
        event_mode = int(event_mode, 16)
        duration = int(duration, 16)
        amount = int(amount, 16)
        user_limit = int(user_limit, 16)
    except ValueError:
        return
    
    duration = TimeDelta(seconds = duration)
    
    message = await client.interaction_response_message_create(
        interaction_event,
        components = build_event_active_components(event_mode, duration, amount, user_limit, None, True),
    )
    
    session = Session(client, message, event_mode, duration, amount, user_limit)
    SESSIONS[message.id] = session
    ensure_session(session)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_EVENT_INACTIVE)
async def handle_dummy():
    """
    Dummy interaction event handler.
    
    This function is a coroutine.
    """
    pass


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_EVENT_ACTIVE)
async def handle_click(
    client,
    interaction_event,
):
    """
    Handles an interaction click.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    try:
        session = SESSIONS[interaction_event.message.id]
    except KeyError:
        return
    
    # Add user id & exit if already used
    user_limit = session.user_limit
    user_id = interaction_event.user.id
    
    if user_limit:
        user_ids = session.user_ids
        if (user_ids is None):
            session.user_ids = user_ids = set()
        elif user_id in user_ids:
            return
        
        user_ids.add(user_id)
    
    # Step the session
    await step_session(session, interaction_event)
    
    # Reward the user.
    user_balance = await get_user_balance(user_id)
    event_mode = session.event_mode
    
    if event_mode == EVENT_MODE_HEART:
        user_balance.modify_balance_by(session.amount)
    
    elif event_mode == EVENT_MODE_STREAK:
        streak, daily_can_claim_at = calculate_daily_new(
            user_balance.streak, user_balance.daily_can_claim_at, DateTime.now(TimeZone.utc)
        )
        user_balance.set_streak(streak + session.amount)
        user_balance.set_daily_can_claim_at(daily_can_claim_at)
    
    else:
        # no other cases.
        pass
    
    await save_user_balance(user_balance)
    
    # Respond
    await client.interaction_followup_message_create(
        interaction_event,
        content = EMOJI__HEART_CURRENCY.as_emoji,
        show_for_invoking_user_only = True,
    )
