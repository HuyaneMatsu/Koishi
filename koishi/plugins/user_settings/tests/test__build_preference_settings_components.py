import vampytest
from hata import Component, User, create_text_display

from ..builders import build_preference_settings_components
from ..constants import (
    PREFERRED_CLIENT_NAME_DEFAULT, PREFERRED_IMAGE_SOURCE_TOUHOU, PREFERRED_IMAGE_SOURCE_NAME_NONE,
    PREFERRED_IMAGE_SOURCE_NAME_TOUHOU
)
from ..user_settings import UserSettings


def _iter_options():
    user_id = 202404270001
    
    user_settings = UserSettings(
        user_id,
        preferred_client_id = 202404270002,
        preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU,
    )
    
    yield (
        user_settings,
        0,
        {},
        [
            create_text_display(
                f'- Preferred client: {PREFERRED_CLIENT_NAME_DEFAULT!s}\n'
                f'- Preferred image source: {PREFERRED_IMAGE_SOURCE_NAME_TOUHOU!s}'
            ),
        ],
    )
    
    user_id = 202402250012
    preferred_client_id = 202402250014
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
        [
            create_text_display(
                f'- Preferred client: {preferred_client_name!s}\n'
                f'- Preferred image source: {PREFERRED_IMAGE_SOURCE_NAME_NONE!s}'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_preference_settings_components(user_settings, guild_id, clients_patch):
    """
    Tests whether ``build_preference_settings_components`` works as intended.
    
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
    output : ``list<Component>``
    """
    mocked = vampytest.mock_globals(
        build_preference_settings_components,
        CLIENTS = clients_patch,
        recursion = 2,
    )
    
    output = mocked(user_settings, guild_id)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
