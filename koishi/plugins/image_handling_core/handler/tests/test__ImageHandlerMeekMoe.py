from collections import deque as Deque

import vampytest
from scarletio import Task

from ...image_detail import ImageDetailBase

from ..meek_moe import ImageHandlerMeekMoe, PROVIDER_MEEK_MOE


def _assert_fields_set(image_handler):
    """
    Asserts whether every fields are set of the given image handler.
    
    Parameters
    ----------
    image_handler : ``ImageHandlerMeekMoe``
        The image handler to check.
    """
    vampytest.assert_instance(image_handler, ImageHandlerMeekMoe)
    vampytest.assert_instance(image_handler._cache, list)
    vampytest.assert_instance(image_handler._request_task, Task, nullable = True)
    vampytest.assert_instance(image_handler._vocaloid_type, str)
    vampytest.assert_instance(image_handler._waiters, Deque)
    

def test__ImageHandlerMeekMoe__new():
    """
    Asserts whether ``ImageHandlerMeekMoe.__new__`` works as intended.
    """
    vocaloid_type = 'alice'
    
    image_handler = ImageHandlerMeekMoe(vocaloid_type)
    _assert_fields_set(image_handler)
    
    vampytest.assert_eq(image_handler._vocaloid_type, vocaloid_type)


def _iter_options__cg_get_image():
    vocaloid_type = 'alice'
    
    yield (
        {
            'vocaloid_type': vocaloid_type,
        },
        None,
        None,
        [None, None],
    )
    
    image_detail = ImageDetailBase(
        'https://www.orindance.party/',
    ).with_provider(
        PROVIDER_MEEK_MOE,
    )
    
    yield (
        {
            'vocaloid_type': vocaloid_type,
        },
        [
            ('_cache', [image_detail]),
        ],
        None,
        [image_detail],
    )
    
    yield (
        {
            'vocaloid_type': vocaloid_type,
        },
        None,
        [image_detail],
        [None, image_detail],
    )


@vampytest._(vampytest.call_from(_iter_options__cg_get_image()).returning_last())
async def test__ImageHandlerMeekMoe__cg_get_image(keyword_parameters, attributes_to_set, request_return):
    """
    Tests whether ``ImageHandlerMeekMoe.cg_get_image`` works as intended.
    
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
    
    image_handler = ImageHandlerMeekMoe(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    original_request = ImageHandlerMeekMoe._request
    ImageHandlerMeekMoe._request = patched_request
    
    try:
        output = []
        async for image_detail in image_handler.cg_get_image():
            vampytest.assert_instance(image_detail, ImageDetailBase, nullable = True)
            output.append(image_detail)
    
    finally:
        ImageHandlerMeekMoe._request = original_request
        
    return output


def _iter_options__eq():
    vocaloid_type = 'alice'
    
    keyword_parameters = {
        'vocaloid_type':vocaloid_type,
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
            'vocaloid_type': 'rin',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ImageHandlerMeekMoe__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ImageHandlerMeekMoe.__eq__`` works as intended.
    
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
    image_handler_0 = ImageHandlerMeekMoe(**keyword_parameters_0)
    image_handler_1 = ImageHandlerMeekMoe(**keyword_parameters_1)
    
    output = image_handler_0 == image_handler_1
    vampytest.assert_instance(output, bool)
    return output
