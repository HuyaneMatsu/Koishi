__all__ = ()

from hata import create_button, create_media_gallery, create_row, create_text_display

from config import FLANDRE_ID

from ..user_settings import USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_DISABLE


IMAGE_ORIN_POKE = 'https://cdn.discordapp.com/attachments/568837922288173058/1211958360107257856/orin-poke-0000.png'
IMAGE_FLANDRE_HAPPY = 'https://cdn.discordapp.com/attachments/568837922288173058/1213514905093804213/flandre-happy-0000.png'


def _notification_builder_daily_reminder_default():
    """
    Default notification builder for daily reminding.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('Hey mister, did you forget your daily?'),
        create_media_gallery(IMAGE_ORIN_POKE),
        create_row(
            create_button(
                'I don\'t want notifs, nya!!',
                custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_DISABLE,
            ),
        ),
    ]


def _notification_builder_daily_reminder_flandre():
    """
    Notification builder for daily reminding for Flandre.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('Onee-sama, did you forget your daily?'),
        create_media_gallery(IMAGE_FLANDRE_HAPPY),
        create_row(
            create_button(
                'Go back to your basement!!',
                custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_REMINDER_DISABLE,
            ),
        ),
    ]


NOTIFICATION_BUILDERS_DAILY_REMINDER = {
    FLANDRE_ID: _notification_builder_daily_reminder_flandre,
}


def build_notification_components(preferred_client_id):
    """
    Builds daily reminder notification components.
    
    Parameters
    ----------
    preferred_client_id : `int`
        The notifier client's identifier to select style for.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return NOTIFICATION_BUILDERS_DAILY_REMINDER.get(
        preferred_client_id, _notification_builder_daily_reminder_default
    )()
