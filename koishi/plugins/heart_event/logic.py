__all__ = ()

from datetime import timedelta as TimeDelta

from hata import KOKORO
from scarletio import LOOP_TIME, Task

from .component_building import build_event_active_components
from .constants import SESSIONS, STEP_INTERVAL


def ensure_session(session):
    """
    Ensures the session's next step.
    
    Parameters
    ----------
    session : ``Session``
    """
    next_update_occurs_at = min(LOOP_TIME() + STEP_INTERVAL, session.ends_at_loop_time)
    update_handle = session.update_handle
    if (update_handle is not None):
        update_handle.cancel()
    
    session.update_handle = KOKORO.call_at(next_update_occurs_at, invoke_step_session, session.message.id)


def invoke_step_session(session_id):
    """
    Invokes the session's step.
    
    Parameters
    ----------
    session_id : `int`
        The session's identifier.
    """
    try:
        session = SESSIONS[session_id]
    except KeyError:
        return
    
    Task(KOKORO, step_session(session, None))


async def step_session(session, interaction_event):
    """
    Steps the session.
    
    This function is a coroutine.
    
    Parameters
    ----------
    session : ``Session``
        Session to step.
    
    interaction_event : ``None | InteractionEvent``
        Interaction event ot respond with if any.
    """
    now = LOOP_TIME()
    
    while True:
        user_limit = session.user_limit
        if user_limit:
            user_ids = session.user_ids
            if (user_ids is not None) and (len(user_ids) >= user_limit):
                duration = 0.0
                active = False
                break
            
        duration = session.ends_at_loop_time - now
        if duration <= 0.0:
            duration = 0.0
            active = False
            break
        
        active = True
        break
    
    if not active:
        try:
            del SESSIONS[session.message.id]
        except KeyError:
            pass
    
    components = build_event_active_components(
        session.event_mode,
        TimeDelta(seconds = duration),
        session.amount,
        session.user_limit,
        session.user_ids,
        active,
    )
    
    try:
        if interaction_event is None:
            await session.client.message_edit(
                session.message,
                components = components,
            )
        
        else:
            await session.client.interaction_response_message_edit(
                interaction_event,
                components = components
            )
    except ConnectionError:
        pass
    
    if active:
        ensure_session(session)
