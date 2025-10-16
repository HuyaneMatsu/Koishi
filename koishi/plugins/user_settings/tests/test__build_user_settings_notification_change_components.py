import vampytest
from hata import Component, create_text_display

from ..builders import build_user_settings_notification_change_components
from ..options import OPTION_NOTIFICATION_DAILY_BY_WAIFU, OPTION_NOTIFICATION_PROPOSAL


def _iter_options():
    yield (
        OPTION_NOTIFICATION_DAILY_BY_WAIFU,
        True,
        True,
        [
            create_text_display('From now on, you will receive daily-by-waifu notifications.')
        ],
    )
    
    yield (
        OPTION_NOTIFICATION_PROPOSAL,
        False,
        False,
        [
            create_text_display('You were already **not** receiving proposal notifications.'),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_settings_notification_change_components(option, value, changed):
    """
    Tests whether ``build_user_settings_notification_change_components`` works as intended.
    
    Parameters
    ----------
    option : ``NotificationOption``
        Option representing the changed notification setting.
    
    value : `bool`
        The new value to set.
    
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_user_settings_notification_change_components(option, value, changed)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
