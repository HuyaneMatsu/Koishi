import vampytest
from hata import Embed, User

from ..builders import build_preference_settings_embed
from ..constants import PREFERRED_CLIENT_NAME_DEFAULT, PREFERRED_IMAGE_SOURCE_TOUHOU, PREFERRED_IMAGE_SOURCE_NAME_TOUHOU
from ..user_settings import UserSettings


def test__build_preference_settings_embed():
    """
    Tests whether ``build_preference_settings_embed`` works as intended.
    """
    user_id = 202404270001
    
    user_settings = UserSettings(
        user_id,
        preferred_client_id = 202404270002,
        preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU,
    )
    
    user = User.precreate(user_id)
    
    expected_output = Embed(
        'Preference settings',
    ).add_thumbnail(
        user.avatar_url,
    ).add_field(
        'Preferred client',
        (
            f'```\n'
            f'{PREFERRED_CLIENT_NAME_DEFAULT!s}\n'
            f'```'
        ),
    ).add_field(
        'Preferred image source',
        (
            f'```\n'
            f'{PREFERRED_IMAGE_SOURCE_NAME_TOUHOU!s}\n'
            f'```'
        ),
    )
        
    
    output = build_preference_settings_embed(user, user_settings)
    vampytest.assert_instance(output, Embed)
    vampytest.assert_eq(output, expected_output)


def test__build_preference_settings_embed__field_preferred_set():
    """
    Tests whether ``build_preference_settings_embed`` works as intended.
    
    Case: Notifier set.
    """
    user_id = 202402250012
    preferred_client_id = 202402250014
    preferred_client_name = 'pudding'
    
    user_settings = UserSettings(
        user_id,
        preferred_client_id = preferred_client_id,
    )
    
    user = User.precreate(user_id)
    preferred_client = User.precreate(preferred_client_id, name = preferred_client_name)
    
    expected_embed_field_value = (
        f'```\n'
        f'{preferred_client_name!s}\n'
        f'```'        
    )
    
    mocked = vampytest.mock_globals(build_preference_settings_embed, CLIENTS = {preferred_client_id: preferred_client})
    
    output = mocked(user, user_settings)
    vampytest.assert_instance(output, Embed)
    
    for field in output.iter_fields():
        if field.name.casefold() == 'preferred client':
            break
    else:
        field = None
    
    vampytest.assert_is_not(field, None)
    vampytest.assert_eq(field.value, expected_embed_field_value)
