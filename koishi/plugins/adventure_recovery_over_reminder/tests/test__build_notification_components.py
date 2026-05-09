import vampytest
from hata import Component, create_button, create_row, create_text_display

from config import ORIN_ID

from ..component_building import build_notification_components


def _iter_options():
    yield (
        'default',
        0,
        [
            create_text_display('Hey mister, you look all recovered!'),
            create_row(
                create_button(
                    'I don\'t want notifs, nya!!',
                    custom_id = 'user_settings.adventure_recovery_over.disable',
                ),
            ),
        ],
    )
    
    yield (
        'default',
        ORIN_ID,
        [
            create_text_display(
                'I am pleased to inform you, that you are all well rested and ready to head out on a corpse voyage.\n'
                'We shall meet once again, when either your cart is full, or when cart is full of you.'
            ),
            create_row(
                create_button(
                    'I do not deserve such notifications.',
                    custom_id = 'user_settings.adventure_recovery_over.disable',
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
