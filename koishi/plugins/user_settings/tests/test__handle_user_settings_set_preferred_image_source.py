import vampytest
from hata import Embed, InteractionEvent, User
from hata.ext.slash import InteractionResponse

from ..constants import (
    PREFERRED_IMAGE_SOURCE_NAME_TOUHOU, PREFERRED_IMAGE_SOURCE_TOUHOU, PREFERRED_IMAGE_SOURCE_WAIFU_PICS
)
from ..user_settings import UserSettings
from ..utils import handle_user_settings_set_preferred_image_source


async def test__handle_user_settings_set_preferred_image_source():
    """
    Tests whether ``build_user_settings_preferred_image_source_change_embed`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 202404280013
    
    user_settings = UserSettings(
        user_id,
        preferred_image_source = PREFERRED_IMAGE_SOURCE_WAIFU_PICS,
    )
    expected_saved_user_settings = UserSettings(
        user_id,
        preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU,
    )
    
    user = User.precreate(user_id)
    
    event = InteractionEvent(
        user = user,
    )
    value = PREFERRED_IMAGE_SOURCE_TOUHOU
    
    get_query_called = False
    save_query_called = False
    
    
    async def get_query(input_user_id):
        nonlocal get_query_called
        nonlocal user_id
        nonlocal user_settings
        
        get_query_called = True
        
        vampytest.assert_eq(input_user_id, user_id)
        
        return user_settings
    
    
    async def save_query(input_user_settings):
        nonlocal save_query_called
        nonlocal expected_saved_user_settings
        
        vampytest.assert_eq(input_user_settings, expected_saved_user_settings)
        
        save_query_called = True
    
    
    mocked = vampytest.mock_globals(
        handle_user_settings_set_preferred_image_source,
        2,
        get_one_user_settings = get_query,
        save_one_user_settings = save_query,
    )
    
    output = await mocked(event, value)
    vampytest.assert_instance(output, InteractionResponse)
    vampytest.assert_true(get_query_called)
    vampytest.assert_true(save_query_called)
    
    vampytest.assert_eq(
        output,
        InteractionResponse(
            embed = Embed(
                'Great success!',
                f'Preferred image source set to `{PREFERRED_IMAGE_SOURCE_NAME_TOUHOU!s}`.',
            ).add_thumbnail(
                user.avatar_url,
            ),
            show_for_invoking_user_only = True,
        ),
    )
