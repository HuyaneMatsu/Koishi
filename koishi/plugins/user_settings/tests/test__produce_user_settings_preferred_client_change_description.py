import vampytest
from hata import User

from ..constants import PREFERRED_CLIENT_NAME_DEFAULT
from ..builders import produce_user_settings_preferred_client_change_description


def _iter_options():
    client_name = 'satori'
    client = User.precreate(202402260008, name = client_name)
    
    yield (
        None,
        0,
        False,
        False,
        'Could not match any available clients.',
    )
    
    yield (
        None,
        0,
        True,
        False,
        f'Preferred client was already `{PREFERRED_CLIENT_NAME_DEFAULT!s}`.',
    )
    
    yield (
        None,
        0,
        True,
        True,
        f'Preferred client set to `{PREFERRED_CLIENT_NAME_DEFAULT!s}`.',
    )
    
    yield (
        client,
        0,
        True,
        False,
        f'Preferred client was already `{client_name!s}`.',
    )
    
    yield (
        client,
        0,
        True,
        True,
        f'Preferred client set to `{client_name!s}`.',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_user_settings_preferred_client_change_description(client, guild_id, value, changed):
    """
    Tests whether ``produce_user_settings_preferred_client_change_description`` works as intended.
    
    Parameters
    ----------
    client : ``None | ClientUserBase``
        The client the notification settings were set to.
    
    guild_id : `int`
        The local guild's identifier.
    
    hit : `bool`
        Whether a client option was hit by the user's input.
    
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_user_settings_preferred_client_change_description(client, guild_id, value, changed)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
