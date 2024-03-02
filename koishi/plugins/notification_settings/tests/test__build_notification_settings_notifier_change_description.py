import vampytest
from hata import User

from ..constants import NOTIFIER_NAME_DEFAULT
from ..builders import build_notification_settings_notifier_change_description


def _iter_options():
    client_name = 'satori'
    client = User.precreate(202402260008, name = client_name)
    
    yield None, False, False, 'Could not match any available clients.'
    yield None, True, False, f'Notifier was already `{NOTIFIER_NAME_DEFAULT!s}`.'
    yield None, True, True, f'Notifier set to `{NOTIFIER_NAME_DEFAULT!s}`.'
    yield client, True, False, f'Notifier was already `{client_name!s}`.'
    yield client, True, True, f'Notifier set to `{client_name!s}`.'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_notification_settings_notifier_change_description(option, value, changed):
    """
    Tests whether ``build_notification_settings_notifier_change_description`` works as intended.
    
    Parameters
    ----------
    client : `None | ClientUserBase`
        The client the notification settings were set to.
    hit : `bool`
        Whether a client option was hit by the user's input.
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    output : `str`
    """
    return build_notification_settings_notifier_change_description(option, value, changed)
