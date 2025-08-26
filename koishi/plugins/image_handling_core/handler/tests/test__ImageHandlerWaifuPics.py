from collections import deque as Deque

import vampytest
from scarletio import Task

from ...image_detail import ImageDetailBase

from ..waifu_pics import ImageHandlerWaifuPics, PROVIDER_WAIFU_PICS


def _assert_fields_set(image_handler):
    """
    Asserts whether every fields are set of the given image handler.
    
    Parameters
    ----------
    image_handler : ``ImageHandlerWaifuPics``
        The image handler to check.
    """
    vampytest.assert_instance(image_handler, ImageHandlerWaifuPics)
    vampytest.assert_instance(image_handler._cache, list)
    vampytest.assert_instance(image_handler._request_task, Task, nullable = True)
    vampytest.assert_instance(image_handler._safe, bool)
    vampytest.assert_instance(image_handler._waifu_type, str)
    vampytest.assert_instance(image_handler._waiters, Deque)
    

def test__ImageHandlerWaifuPics__new():
    """
    Asserts whether ``ImageHandlerWaifuPics.__new__`` works as intended.
    """
    safe = True
    waifu_type = 'trap'
    
    image_handler = ImageHandlerWaifuPics(waifu_type, safe)
    _assert_fields_set(image_handler)
    
    vampytest.assert_eq(image_handler._safe, safe)
    vampytest.assert_eq(image_handler._waifu_type, waifu_type)


def _iter_options__cg_get_image():
    safe = True
    waifu_type = 'trap'
    
    yield (
        {
            'safe': safe,
            'waifu_type': waifu_type,
        },
        None,
        None,
        [None, None],
    )
    
    image_detail = ImageDetailBase(
        'https://www.orindance.party/',
    ).with_provider(
        PROVIDER_WAIFU_PICS,
    )
    
    yield (
        {
            'safe': safe,
            'waifu_type': waifu_type,
        },
        [
            ('_cache', [image_detail]),
        ],
        None,
        [image_detail],
    )
    
    yield (
        {
            'safe': safe,
            'waifu_type': waifu_type,
        },
        None,
        [image_detail],
        [None, image_detail],
    )


@vampytest._(vampytest.call_from(_iter_options__cg_get_image()).returning_last())
async def test__ImageHandlerWaifuPics__cg_get_image(keyword_parameters, attributes_to_set, request_return):
    """
    Tests whether ``ImageHandlerWaifuPics.cg_get_image`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    request_return : ``None | list<ImageDetailBase>``
        Image details return from request.
    
    Returns
    -------
    output : ``list<None | ImageDetailBase>``
    """
    async def patched_request(instance):
        nonlocal request_return
        return request_return
    
    image_handler = ImageHandlerWaifuPics(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    original_request = ImageHandlerWaifuPics._request
    ImageHandlerWaifuPics._request = patched_request
    
    try:
        output = []
        async for image_detail in image_handler.cg_get_image():
            vampytest.assert_instance(image_detail, ImageDetailBase, nullable = True)
            output.append(image_detail)
    
    finally:
        ImageHandlerWaifuPics._request = original_request
        
    return output


def _iter_options__eq():
    safe = True
    waifu_type = 'trap'
    
    keyword_parameters = {
        'safe': safe,
        'waifu_type': waifu_type,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'safe': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'waifu_type': 'awoo',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ImageHandlerWaifuPics__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ImageHandlerWaifuPics.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    image_handler_0 = ImageHandlerWaifuPics(**keyword_parameters_0)
    image_handler_1 = ImageHandlerWaifuPics(**keyword_parameters_1)
    
    output = image_handler_0 == image_handler_1
    vampytest.assert_instance(output, bool)
    return output
