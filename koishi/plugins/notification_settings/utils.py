__all__ = ('handle_notification_settings_change', )

from hata.ext.slash import InteractionResponse

from .builders import build_notification_settings_change_embed
from .queries import get_one_notification_settings, save_one_notification_settings


async def set_notification_settings_option(notification_settings, option, value):
    """
    Sets a notification settings option to the given value.
    
    Parameters
    ----------
    notification_settings : ``NotificationSettings``
        The notification settings to modify.
    option : ``NotificationSettingsOption``
        Its option to modify.
    value : `bool`
        The value to set.
    
    Returns
    -------
    changed : `bool`
    """
    actual = option.get(notification_settings)
    if actual == value:
        return False
    
    option.set(notification_settings, value)
    await save_one_notification_settings(notification_settings)
    return True


async def handle_notification_settings_change(event, option, value):
    """
    handles a notification settings change.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    option : ``NotificationOption``
        Option representing the changed notification setting.
    value : `bool`
        The new value to set.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    notification_settings = await get_one_notification_settings(event.user.id)
    changed = await set_notification_settings_option(notification_settings, option, value)
    return InteractionResponse(
        embed = build_notification_settings_change_embed(event.user, option, value, changed),
        show_for_invoking_user_only = True,
    )
