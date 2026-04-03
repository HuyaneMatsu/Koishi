from collections import deque as Deque

import vampytest
from scarletio import Task

from ...image_detail import ImageDetailBase

from ..dan_booru import ImageHandlerDanBooru, PROVIDER_DAN_BOORU


def _assert_fields_set(image_handler):
    """
    Asserts whether every fields are set of the given image handler.
    
    Parameters
    ----------
    image_handler : ``ImageHandlerDanBooru``
        The image handler to check.
    """
    vampytest.assert_instance(image_handler, ImageHandlerDanBooru)
    vampytest.assert_instance(image_handler._cache, list)
    vampytest.assert_instance(image_handler._page, int)
    vampytest.assert_instance(image_handler._random_order, bool)
    vampytest.assert_instance(image_handler._request_task, Task, nullable = True)
    vampytest.assert_instance(image_handler._tags_banned, frozenset, nullable = True)
    vampytest.assert_instance(image_handler._tags_joined, str)
    vampytest.assert_instance(image_handler._tags_joined_raw, str)
    vampytest.assert_instance(image_handler._tags_required, frozenset, nullable = True)
    vampytest.assert_instance(image_handler._waiters, Deque)
    

def test__ImageHandlerDanBooru__new():
    """
    Asserts whether ``ImageHandlerDanBooru.__new__`` works as intended.
    """
    tags_required = frozenset((
        'touhou',
        'solo',
    ))
    
    tags_banned = frozenset((
        'smoking',
        'bikini',
    ))
    
    tags_requested = {
        (True, 'komeiji_koishi'),
        (False, 'komeiji_satori'),
    }
    
    random_order = True
    
    image_handler = ImageHandlerDanBooru(tags_required, tags_banned, tags_requested, random_order)
    _assert_fields_set(image_handler)
    
    vampytest.assert_eq(image_handler._random_order, random_order)
    vampytest.assert_eq(image_handler._tags_banned, tags_banned)
    vampytest.assert_eq(image_handler._tags_joined, '-bikini -komeiji_satori -smoking komeiji_koishi solo touhou')
    vampytest.assert_eq(image_handler._tags_joined_raw, '-komeiji_satori komeiji_koishi')
    vampytest.assert_eq(image_handler._tags_required, tags_required)


def _iter_options__cg_get_image():
    tags_required = frozenset((
        'touhou',
        'solo',
    ))
    
    tags_banned = frozenset((
        'smoking',
        'bikini',
    ))
    
    tags_requested = {
        (True, 'komeiji_koishi'),
        (False, 'komeiji_satori'),
    }
    
    random_order = True
    
    yield (
        {
            'tags_required': tags_required,
            'tags_banned': tags_banned,
            'tags_requested': tags_requested,
            'random_order': random_order,
        },
        None,
        None,
        [None, None],
    )
    
    image_detail = ImageDetailBase(
        'https://www.orindance.party/',
    ).with_provider(
        PROVIDER_DAN_BOORU,
    ).with_tags(frozenset((
        'komeiji_koishi',
        'solo',
        'touhou',
    )))
    
    yield (
        {
            'tags_required': tags_required,
            'tags_banned': tags_banned,
            'tags_requested': tags_requested,
            'random_order': random_order,
        },
        [
            ('_cache', [image_detail]),
        ],
        None,
        [image_detail],
    )
    
    yield (
        {
            'tags_required': tags_required,
            'tags_banned': tags_banned,
            'tags_requested': tags_requested,
            'random_order': random_order,
        },
        None,
        [image_detail],
        [None, image_detail],
    )


@vampytest._(vampytest.call_from(_iter_options__cg_get_image()).returning_last())
async def test__ImageHandlerDanBooru__cg_get_image(keyword_parameters, attributes_to_set, request_return):
    """
    Tests whether ``ImageHandlerDanBooru.cg_get_image`` works as intended.
    
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
    
    image_handler = ImageHandlerDanBooru(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    original_request = ImageHandlerDanBooru._request
    ImageHandlerDanBooru._request = patched_request
    
    try:
        output = []
        async for image_detail in image_handler.cg_get_image():
            vampytest.assert_instance(image_detail, ImageDetailBase, nullable = True)
            output.append(image_detail)
    
    finally:
        ImageHandlerDanBooru._request = original_request
        
    return output


def _iter_options__eq():
    tags_required = frozenset((
        'touhou',
        'solo',
    ))
    
    tags_banned = frozenset((
        'smoking',
        'bikini',
    ))
    
    tags_requested = {
        (True, 'komeiji_koishi'),
        (False, 'komeiji_satori'),
    }
    
    random_order = True
    
    keyword_parameters = {
        'tags_required': tags_required,
        'tags_banned': tags_banned,
        'tags_requested': tags_requested,
        'random_order': random_order,
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
            'tags_required': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'tags_banned': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'tags_requested': set(),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'random_order': False,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ImageHandlerDanBooru__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ImageHandlerDanBooru.__eq__`` works as intended.
    
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
    image_handler_0 = ImageHandlerDanBooru(**keyword_parameters_0)
    image_handler_1 = ImageHandlerDanBooru(**keyword_parameters_1)
    
    output = image_handler_0 == image_handler_1
    vampytest.assert_instance(output, bool)
    return output
