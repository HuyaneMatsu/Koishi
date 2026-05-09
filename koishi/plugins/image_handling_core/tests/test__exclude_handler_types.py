import vampytest

from ...user_settings import PREFERRED_IMAGE_SOURCE_NONE, PREFERRED_IMAGE_SOURCE_TOUHOU

from ..handler import ImageHandlerBase, ImageHandlerGroup, ImageHandlerStatic, ImageHandlerWaifuPics
from ..utils import exclude_handler_types


def _iter_options():
    image_handler_waifu_pics = ImageHandlerWaifuPics('awoo', True)
    image_handler_static_0 = ImageHandlerStatic(PREFERRED_IMAGE_SOURCE_TOUHOU, None)
    image_handler_static_1 = ImageHandlerStatic(PREFERRED_IMAGE_SOURCE_NONE, None)
    
    image_handler_group_0 = ImageHandlerGroup(
        image_handler_waifu_pics,
        image_handler_static_0,
    )
    
    image_handler_group_1 = ImageHandlerGroup(
        image_handler_static_0,
        image_handler_static_1,
    )
    
    yield (
        image_handler_waifu_pics,
        (
            ImageHandlerBase,
        ),
        None,
    )
    
    yield (
        image_handler_waifu_pics,
        (
            ImageHandlerWaifuPics,
        ),
        None,
    )
    
    yield (
        image_handler_waifu_pics,
        (
            ImageHandlerStatic,
        ),
        image_handler_waifu_pics,
    )
    
    yield (
        image_handler_static_0,
        (
            ImageHandlerStatic,
        ),
        None,
    )
    
    yield (
        image_handler_group_0,
        (
            ImageHandlerStatic,
        ),
        image_handler_waifu_pics,
    )
    
    yield (
        image_handler_group_0,
        (
            ImageHandlerWaifuPics,
        ),
        image_handler_static_0,
    )
    
    yield (
        image_handler_group_1,
        (
            ImageHandlerStatic,
        ),
        None,
    )
    
    yield (
        image_handler_group_1,
        (
            ImageHandlerWaifuPics,
        ),
        image_handler_group_1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__exclude_handler_types(handler, handler_types_to_exclude):
    """
    Tests whether ``exclude_handler_types`` works as intended.
    
    Parameters
    ----------
    handler : ``ImageHandlerBase``
        Handler to exclude from.
    
    handler_types_to_exclude : ``tuple<type<ImageHandlerBase>>``
        Handler types to exclude.
    
    Returns
    -------
    output : ``None | ImageHandlerBase``
    """
    output = exclude_handler_types(handler, handler_types_to_exclude)
    vampytest.assert_instance(output, ImageHandlerBase, nullable = True)
    return output
