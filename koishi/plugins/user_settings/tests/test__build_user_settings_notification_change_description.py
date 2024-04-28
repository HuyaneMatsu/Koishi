import vampytest

from ..builders import build_user_settings_notification_change_description
from ..options import OPTION_NOTIFICATION_DAILY_BY_WAIFU, OPTION_NOTIFICATION_PROPOSAL


def _iter_options():
    yield OPTION_NOTIFICATION_DAILY_BY_WAIFU, True, True, 'From now on, you will receive daily-by-waifu notifications.'
    yield OPTION_NOTIFICATION_PROPOSAL, True, True, 'From now on, you will receive proposal notifications.'
    yield OPTION_NOTIFICATION_PROPOSAL, True, False, 'You were already receiving proposal notifications.'
    yield OPTION_NOTIFICATION_PROPOSAL, False, True, 'From now, you will **not** receive proposal notifications.'
    yield OPTION_NOTIFICATION_PROPOSAL, False, False, 'You were already **not** receiving proposal notifications.'
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_settings_notification_change_description(option, value, changed):
    """
    Tests whether ``build_user_settings_notification_change_description`` works as intended.
    
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
    output : `str`
    """
    return build_user_settings_notification_change_description(option, value, changed)
