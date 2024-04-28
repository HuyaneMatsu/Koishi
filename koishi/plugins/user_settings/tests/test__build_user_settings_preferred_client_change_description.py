import vampytest
from hata import User

from ..constants import PREFERRED_CLIENT_NAME_DEFAULT
from ..builders import build_user_settings_preferred_client_change_description


def _iter_options():
    client_name = 'satori'
    client = User.precreate(202402260008, name = client_name)
    
    yield None, False, False, 'Could not match any available clients.'
    yield None, True, False, f'Preferred client was already `{PREFERRED_CLIENT_NAME_DEFAULT!s}`.'
    yield None, True, True, f'Preferred client set to `{PREFERRED_CLIENT_NAME_DEFAULT!s}`.'
    yield client, True, False, f'Preferred client was already `{client_name!s}`.'
    yield client, True, True, f'Preferred client set to `{client_name!s}`.'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_settings_preferred_client_change_description(option, value, changed):
    """
    Tests whether ``build_user_settings_preferred_client_change_description`` works as intended.
    
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
    return build_user_settings_preferred_client_change_description(option, value, changed)
