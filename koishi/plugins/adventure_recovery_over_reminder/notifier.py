__all__ = ()

from ..reminder_notification_delivery_core import try_channel_create, try_message_create, try_user_get
from ..user_settings import get_preferred_client_for_user

from .component_building import build_notification_components
from .queries import set_entry_as_delayed_with_connector, set_entry_as_notified_with_connector


async def notify_user(entry, connector):
    """
    Notifies the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry : `sqlalchemy.engine.result.RowProxy<id: int, user_id: int, preferred_client_id: int>`
        The entry representing a user and its configuration to notify.
    
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    success : `bool`
    """
    entry_id, user_id, preferred_client_id = entry
    
    while True:
        user, set_as_notified = await try_user_get(user_id)
        if user is None:
            success = False
            break
        
        client = get_preferred_client_for_user(user, preferred_client_id, None)
        channel, set_as_notified = await try_channel_create(client, user_id)
        if channel is None:
            success = False
            break
        
        components = build_notification_components(preferred_client_id)
        message, set_as_notified = await try_message_create(client, channel, components)
        if message is None:
            success = False
            break
        
        set_as_notified = True
        success = True
        break
    
    await (set_entry_as_notified_with_connector if set_as_notified else set_entry_as_delayed_with_connector)(
        connector, entry_id
    )
    
    return success
