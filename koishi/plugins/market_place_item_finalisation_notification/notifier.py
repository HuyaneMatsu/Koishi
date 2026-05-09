__all__ = ()

from ..user_settings import get_preferred_client_for_user


from ..reminder_notification_delivery_core import try_channel_create, try_message_create, try_user_get

from .component_building import build_notification_components
from .queries import set_entry_as_notified_with_connector


async def notify_user(entry, connector):
    """
    Notifies the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry : `sqlalchemy.engine.result.RowProxy<>`
        The entry representing a user and its configuration to notify.
    
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    success : `bool`
    """
    (
        entry_id,
        flags,
        seller_user_id,
        purchaser_user_id,
        item_id,
        item_amount,
        seller_balance_amount,
        purchaser_balance_amount,
        user_id,
        preferred_client_id
    ) = entry
    
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
        
        components = build_notification_components(
            preferred_client_id,
            user_id,
            seller_user_id,
            purchaser_user_id,
            item_id,
            item_amount,
            seller_balance_amount,
            purchaser_balance_amount,
        )
        message, set_as_notified = await try_message_create(client, channel, components)
        if message is None:
            success = False
            break
        
        set_as_notified = True
        success = True
        break
    
    if set_as_notified:
        await set_entry_as_notified_with_connector(connector, entry_id, seller_user_id == user_id)
    
    return success
