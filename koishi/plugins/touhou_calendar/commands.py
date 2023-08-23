__all__ = ()

import re
from datetime import datetime as DateTime

from hata import Client

from ...bots import SLASH_CLIENT

from .constants import CUSTOM_ID_BACK_DISABLED, CUSTOM_ID_CLOSE, CUSTOM_ID_NEXT_DISABLED
from .response_building import get_response_for_year


@SLASH_CLIENT.interactions(is_global = True)
async def touhou_calendar():
    """
    Returns the touhou calendar for the current year.
    
    This function is a coroutine.
    
    Parameters
    ----------
    month : `int` = `-1`, Optional (Keyword only)
        The month to get the calendar for.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    return get_response_for_year(DateTime.utcnow().year)


@SLASH_CLIENT.interactions(custom_id = re.compile('touhou_calendar.year.(\d+)'))
async def touhou_calendar_page(client, event, year):
    """
    Returns the touhou calendar for the given year.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    year : `str`
        The year to get the calendar for. Later converted to `int`.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    if event.message.interaction.user is not event.user:
        await client.interaction_component_acknowledge(event)
        await client.interaction_followup_message_create(
            event,
            'You must be the original invoker of the command to do this.',
            show_for_invoking_user_only = True,
        )
        return
    
    return get_response_for_year(int(year))


@SLASH_CLIENT.interactions(custom_id = [CUSTOM_ID_BACK_DISABLED, CUSTOM_ID_NEXT_DISABLED])
async def touhou_calendar_page_disabled():
    """
    Handles a disabled component click. So does nothing.
    
    This function is a coroutine.
    """


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_CLOSE)
async def touhou_calendar_close(client, event):
    """
    Deletes the calendar message if applicable.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event)
    
    if event.user_permissions.can_manage_messages or event.message.interaction.user is event.user:
        await client.interaction_response_message_delete(event)
    
    else:
        await client.interaction_followup_message_create(
            event,
            'You must be the invoker of the interaction, or have manage messages permission to do this.',
            show_for_invoking_user_only = True,
        )
