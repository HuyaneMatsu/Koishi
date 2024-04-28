__all__ = ()

from hata import Embed
from hata.ext.slash import Button

from config import FLANDRE_ID

from ..user_settings import USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_DISABLE


IMAGE_ORIN_POKE = 'https://cdn.discordapp.com/attachments/568837922288173058/1211958360107257856/orin-poke-0000.png'
IMAGE_FLANDRE_HAPPY = 'https://cdn.discordapp.com/attachments/568837922288173058/1213514905093804213/flandre-happy-0000.png'


def _notification_builder_daily_reminder_default():
    """
    Default notification builder for daily reminding.
    
    Returns
    -------
    embed : ``Embed``
    components : ``Component``
    """
    return (
        Embed(
            description = 'Hey mister, did you forget your daily?',
        ).add_thumbnail(
            IMAGE_ORIN_POKE,
        ),
        Button(
            'I don\'t want notifs, nya!!',
            custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_DISABLE,
        ),
    )


def _notification_builder_daily_reminder_flandre():
    """
    Notification builder for daily reminding for Flandre.
    
    Returns
    -------
    embed : ``Embed``
    components : ``Component``
    """
    return (
        Embed(
            description = 'Onee-sama, did you forget your daily?',
        ).add_thumbnail(
            IMAGE_FLANDRE_HAPPY,
        ),
        Button(
            'Go back to your basement!!',
            custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_DISABLE,
        ),
    )


NOTIFICATION_BUILDERS_DAILY_REMINDER = {
    FLANDRE_ID: _notification_builder_daily_reminder_flandre,
}


def build_notification_daily_reminder(preferred_client_id):
    """
    Notification builder for daily reminder.
    
    Parameters
    ----------
    preferred_client_id : `int`
        The notifier client's identifier to select style for.
    
    Returns
    -------
    embed : ``Embed``
    components : ``Component``
    """
    notification_builder = NOTIFICATION_BUILDERS_DAILY_REMINDER.get(
        preferred_client_id, _notification_builder_daily_reminder_default
    )
    return notification_builder()
