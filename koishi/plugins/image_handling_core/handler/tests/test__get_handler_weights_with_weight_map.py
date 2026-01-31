import vampytest

from ....user_settings import (
    PREFERRED_IMAGE_SOURCE_NONE, PREFERRED_IMAGE_SOURCE_TOUHOU, PREFERRED_IMAGE_SOURCE_WAIFU_PICS
)

from ..base import ImageHandlerBase
from ..group import get_handler_weights_with_weight_map
from ..waifu_pics import ImageHandlerWaifuPics


def test__get_handler_weights_with_weight_map__undefined_for_handlers():
    """
    Tests whether ``get_handler_weights_with_weight_map`` works as intended.
    
    Case: Using image source weight that is undefined for the handlers.
    """
    image_handler_0 = ImageHandlerBase()
    image_handler_1 = ImageHandlerWaifuPics('awoo', True)
    
    weight_map = {
        PREFERRED_IMAGE_SOURCE_NONE: 1.0,
        PREFERRED_IMAGE_SOURCE_TOUHOU: 2.0,
    }
    
    output = get_handler_weights_with_weight_map([image_handler_0, image_handler_1], weight_map)
    
    vampytest.assert_instance(output, list)
    for value in output:
        vampytest.assert_instance(value, float)
    
    vampytest.assert_eq(
        output,
        [2.0, 1.0],
    )


def test__get_handler_weights_with_weight_map__defined_for_single():
    """
    Tests whether ``get_handler_weights_with_weight_map`` works as intended.
    
    Case: Using the image source only of a single handler.
    """
    image_handler_0 = ImageHandlerBase()
    image_handler_1 = ImageHandlerWaifuPics('awoo', True)
    
    weight_map = {
        PREFERRED_IMAGE_SOURCE_WAIFU_PICS: 2.0,
    }
    
    output = get_handler_weights_with_weight_map([image_handler_0, image_handler_1], weight_map)
    
    vampytest.assert_instance(output, list)
    for value in output:
        vampytest.assert_instance(value, float)
    
    vampytest.assert_eq(
        output,
        [0.0, 2.0],
    )
