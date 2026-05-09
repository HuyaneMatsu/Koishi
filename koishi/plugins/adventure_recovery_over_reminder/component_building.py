__all__ = ()

from hata import create_button, create_row, create_text_display

from config import ORIN_ID

from ..user_settings import USER_SETTINGS_CUSTOM_ID_NOTIFICATION_ADVENTURE_RECOVERY_OVER_DISABLE


def _notification_builder_daily_reminder_default():
    """
    Default notification builder for daily reminding.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display('Hey mister, you look all recovered!'),
        create_row(
            create_button(
                'I don\'t want notifs, nya!!',
                custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_ADVENTURE_RECOVERY_OVER_DISABLE,
            ),
        ),
    ]


def _notification_builder_daily_reminder_orin():
    """
    Notification builder for daily reminding for Orin.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(
            'I am pleased to inform you, that you are all well rested and ready to head out on a corpse voyage.\n'
            'We shall meet once again, when either your cart is full, or when cart is full of you.'
        ),
        create_row(
            create_button(
                'I do not deserve such notifications.',
                custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_ADVENTURE_RECOVERY_OVER_DISABLE,
            ),
        ),
    ]


NOTIFICATION_BUILDERS_ADVENTURE_RECOVERY_OVER = {
    ORIN_ID: _notification_builder_daily_reminder_orin,
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
    return NOTIFICATION_BUILDERS_ADVENTURE_RECOVERY_OVER.get(
        preferred_client_id, _notification_builder_daily_reminder_default
    )()
