import vampytest

from ....user_settings import PREFERRED_IMAGE_SOURCE_TOUHOU

from ..base import ImageHandlerBase
from ..group import get_handler_weights_with_weight_map
from ..waifu_pics import ImageHandlerWaifuPics


def test__get_handler_weights_with_weight_map():
    """
    Tests whether ``get_handler_weights_with_weight_map`` works as intended.
    """
    image_handler_0 = ImageHandlerBase()
    image_handler_1 = ImageHandlerWaifuPics('awoo', False)
    
    weight_map = {
        image_handler_0.get_image_source(): 1.0,
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
