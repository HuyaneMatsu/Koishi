import vampytest
from hata import User

from ..builders import produce_preference_settings_description
from ..constants import (
    PREFERRED_CLIENT_NAME_DEFAULT, PREFERRED_IMAGE_SOURCE_TOUHOU, PREFERRED_IMAGE_SOURCE_NAME_NONE,
    PREFERRED_IMAGE_SOURCE_NAME_TOUHOU
)
from ..user_settings import UserSettings


def _iter_options():
    user_id = 202510080001
    
    user_settings = UserSettings(
        user_id,
        preferred_client_id = 202510080002,
        preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU,
    )
    
    yield (
        user_settings,
        0,
        {},
        (
            f'- Preferred client: {PREFERRED_CLIENT_NAME_DEFAULT!s}\n'
            f'- Preferred image source: {PREFERRED_IMAGE_SOURCE_NAME_TOUHOU!s}'
        ),
    )
    
    user_id = 202510080003
    preferred_client_id = 202510080004
    preferred_client_name = 'pudding'
    preferred_client = User.precreate(
        preferred_client_id,
        name = preferred_client_name,
    )
    
    user_settings = UserSettings(
        user_id,
        preferred_client_id = preferred_client_id,
    )
    
    yield (
        user_settings,
        0,
        {
            preferred_client_id: preferred_client,
        },
        (
            f'- Preferred client: {preferred_client_name!s}\n'
            f'- Preferred image source: {PREFERRED_IMAGE_SOURCE_NAME_NONE!s}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_preference_settings_description(user_settings, guild_id, clients_patch):
    """
    Tests whether ``produce_preference_settings_description`` works as intended.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user's settings.
    
    guild_id : `int`
        The local guild's identifier.
    
    clients_patch : ``dict<int, ClientUserBase>``
        Clients patch.
    
    Returns
    -------
    output : `str`
    """
    mocked = vampytest.mock_globals(
        produce_preference_settings_description,
        CLIENTS = clients_patch,
    )
    
    output = [*mocked(user_settings, guild_id)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
