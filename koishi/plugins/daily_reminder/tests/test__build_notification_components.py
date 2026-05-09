import vampytest
from hata import Component, MediaInfo, MediaItem, create_button, create_media_gallery, create_row, create_text_display

from config import FLANDRE_ID

from ..component_building import IMAGE_FLANDRE_HAPPY, IMAGE_ORIN_POKE, build_notification_components


def _iter_options():
    yield (
        'default',
        0,
        [
            create_text_display('Hey mister, did you forget your daily?'),
            create_media_gallery(
                MediaItem(
                    MediaInfo(
                        IMAGE_ORIN_POKE,
                    ),
                ),
            ),
            create_row(
                create_button(
                    'I don\'t want notifs, nya!!',
                    custom_id = 'user_settings.notification_daily_reminder.disable',
                ),
            ),
        ],
    )
    
    yield (
        'default',
        FLANDRE_ID,
        [
            create_text_display('Onee-sama, did you forget your daily?'),
            create_media_gallery(
                MediaItem(
                    MediaInfo(
                        IMAGE_FLANDRE_HAPPY,
                    ),
                ),
            ),
            create_row(
                create_button(
                    'Go back to your basement!!',
                    custom_id = 'user_settings.notification_daily_reminder.disable',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__build_notification_components(preferred_client_id):
    """
    Tests whether ``build_notification_components``.
    
    Parameters
    ----------
    preferred_client_id : `int`
        The notifier client's identifier to select style for.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_notification_components(preferred_client_id)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
