import vampytest

from ..constants import PREFERRED_IMAGE_SOURCE_NONE, PREFERRED_IMAGE_SOURCE_TOUHOU

from ..user_settings import UserSettings
from ..utils import get_preferred_image_source_weight_map


async def test__get_preferred_image_source_weight_map():
    """
    Tests whether ``get_preferred_image_source_weight_map`` works as intended.
    
    This function is a coroutine.
    """
    user_id_0 = 202404280000
    user_id_1 = 202404280001
    user_id_2 = 202404280002
    user_ids = [user_id_0, user_id_1, user_id_2]
    
    user_settings = [
        UserSettings(user_id_0, preferred_image_source = PREFERRED_IMAGE_SOURCE_NONE),
        UserSettings(user_id_1, preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU),
        UserSettings(user_id_2, preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU),
    ]
    
    async def mock_get_more_user_settings(input_user_ids):
        nonlocal user_ids
        nonlocal user_settings
        
        vampytest.assert_eq(user_ids, input_user_ids)
        return user_settings
    
    
    mocked = vampytest.mock_globals(
        get_preferred_image_source_weight_map,
        get_more_user_settings = mock_get_more_user_settings,
    )
    
    output = await mocked(user_ids)
    
    vampytest.assert_instance(output, dict)
    vampytest.assert_eq(
        output,
        {
            PREFERRED_IMAGE_SOURCE_NONE: 1.0,
            PREFERRED_IMAGE_SOURCE_TOUHOU: 2.0,
        },
    )
