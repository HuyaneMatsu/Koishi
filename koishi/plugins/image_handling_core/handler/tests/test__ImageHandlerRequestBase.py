from collections import deque as Deque

import vampytest
from scarletio import Task

from ...image_detail import ImageDetailBase

from ..request_base import ImageHandlerRequestBase


def _assert_fields_set(image_handler):
    """
    Asserts whether every fields are set of the given image handler.
    
    Parameters
    ----------
    image_handler : ``ImageHandlerRequestBase``
        The image handler to check.
    """
    vampytest.assert_instance(image_handler, ImageHandlerRequestBase)
    vampytest.assert_instance(image_handler._cache, list)
    vampytest.assert_instance(image_handler._request_task, Task, nullable = True)
    vampytest.assert_instance(image_handler._waiters, Deque)
    

def test__ImageHandlerRequestBase__new():
    """
    Asserts whether ``ImageHandlerRequestBase.__new__`` works as intended.
    """
    image_handler = ImageHandlerRequestBase()
    _assert_fields_set(image_handler)


def _iter_options__cg_get_image():
    yield (
        {},
        None,
        None,
        [None, None],
    )
    
    image_detail = ImageDetailBase('https://www.orindance.party/')
    
    yield (
        {},
        [
            ('_cache', [image_detail]),
        ],
        None,
        [image_detail],
    )
    
    image_detail = ImageDetailBase('https://www.orindance.party/')
    
    yield (
        {},
        None,
        [image_detail],
        [None, image_detail],
    )


@vampytest._(vampytest.call_from(_iter_options__cg_get_image()).returning_last())
async def test__ImageHandlerRequestBase__cg_get_image(keyword_parameters, attributes_to_set, request_return):
    """
    Tests whether ``ImageHandlerRequestBase.cg_get_image`` works as intended.
    
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
    
    image_handler = ImageHandlerRequestBase(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    original_request = ImageHandlerRequestBase._request
    ImageHandlerRequestBase._request = patched_request
    
    try:
        output = []
        async for image_detail in image_handler.cg_get_image():
            vampytest.assert_instance(image_detail, ImageDetailBase, nullable = True)
            output.append(image_detail)
    
    finally:
        ImageHandlerRequestBase._request = original_request
        
    return output
