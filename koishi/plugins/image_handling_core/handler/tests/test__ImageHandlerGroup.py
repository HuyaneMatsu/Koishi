import vampytest

from ....user_settings import PREFERRED_IMAGE_SOURCE_NONE, PREFERRED_IMAGE_SOURCE_TOUHOU

from ...image_detail import ImageDetailBase, ImageDetailStatic

from ..base import ImageHandlerBase
from ..group import ImageHandlerGroup
from ..static import ImageHandlerStatic
from ..waifu_pics import ImageHandlerWaifuPics


def _assert_fields_set(image_handler):
    """
    Asserts whether every fields are set of the given image handler.
    
    Parameters
    ----------
    image_handler : ``ImageHandlerGroup``
        The image handler to check.
    """
    vampytest.assert_instance(image_handler, ImageHandlerGroup)
    vampytest.assert_instance(image_handler._handlers, list)
    vampytest.assert_instance(image_handler._weights, list)


def test__ImageHandlerGroup__new():
    """
    Asserts whether ``ImageHandlerGroup.__new__`` works as intended.
    """
    image_handler_0 = ImageHandlerBase()
    image_handler_1 = ImageHandlerWaifuPics('awoo', True)
    
    image_handler = ImageHandlerGroup(
        image_handler_0,
        image_handler_1,
    )
    _assert_fields_set(image_handler)
    
    vampytest.assert_eq(
        image_handler._handlers,
        [
            image_handler_0,
            image_handler_1,
        ],
    )
    
    vampytest.assert_eq(
        image_handler._weights,
        [
            1.0,
            1.0,
        ],
    )


def _iter_options__eq():
    image_handler_0 = ImageHandlerBase()
    image_handler_1 = ImageHandlerWaifuPics('awoo', True)
    
    
    image_handlers = [
        image_handler_0,
        image_handler_1,
    ]
    
    yield (
        image_handlers,
        image_handlers,
        True,
    )
    
    yield (
        image_handlers,
        [
            image_handler_0,
        ],
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ImageHandlerGroup__eq(image_handlers_0, image_handlers_1):
    """
    Tests whether ``ImageHandlerGroup.__eq__`` works as intended.
    
    Parameters
    ----------
    image_handlers_0 : ``list<ImageHandlerBase>``
        Image handlers to create instance with.
    
    image_handlers_1 : ``list<ImageHandlerBase>``
        Image handlers to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    image_handler_0 = ImageHandlerGroup(*image_handlers_0)
    image_handler_1 = ImageHandlerGroup(*image_handlers_1)
    
    output = image_handler_0 == image_handler_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__cg_get_image():
    image_handler_0 = ImageHandlerBase()
    image_handler_1 = ImageHandlerBase()
    
    image_detail_0 = ImageDetailStatic('https://orindance.party/')
    
    image_handler_2 = ImageHandlerStatic(
        PREFERRED_IMAGE_SOURCE_TOUHOU,
        [
            image_detail_0,
        ],
    )
    
    yield (
        [
            
            image_handler_0,
            image_handler_1,
        ],
        None,
        [],
    )
    
    yield (
        [
            image_handler_0,
            image_handler_2,
        ],
        None,
        [
            image_detail_0,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__cg_get_image()).returning_last())
async def test__ImageHandlerGroup__cg_get_image(image_handlers, attributes_to_set):
    """
    Tests whether ``ImageHandlerGroup.cg_get_image`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    image_handlers : ``list<ImageHandlerBase>``
        Image handlers to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    Returns
    -------
    output : ``list<None | ImageDetailBase>``
    """
    image_handler = ImageHandlerGroup(*image_handlers)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = []
    async for image_detail in image_handler.cg_get_image():
        vampytest.assert_instance(image_detail, ImageDetailBase, nullable = True)
        output.append(image_detail)
    
    return output


def _iter_options__cg_get_image_weighted():
    image_detail_0 = ImageDetailStatic('https://orindance.party/')
    image_detail_1 = ImageDetailStatic('https://orindance.party/nyan')
    
    image_handler_0 = ImageHandlerStatic(
        PREFERRED_IMAGE_SOURCE_TOUHOU,
        [
            image_detail_0,
        ],
    )
    
    image_handler_1 = ImageHandlerStatic(
        PREFERRED_IMAGE_SOURCE_NONE,
        [
            image_detail_1,
        ],
    )
    
    yield (
        [
            
            image_handler_0,
            image_handler_1,
        ],
        None,
        {
            PREFERRED_IMAGE_SOURCE_NONE : 1.0,
        },
        [
            image_detail_1,
        ],
    )
    
    yield (
        [
            image_handler_0,
            image_handler_1,
        ],
        None,
        {
            PREFERRED_IMAGE_SOURCE_TOUHOU : 1.0,
        },
        [
            image_detail_0,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__cg_get_image_weighted()).returning_last())
async def test__ImageHandlerGroup__cg_get_image_weighted__no_cache(image_handlers, attributes_to_set, weight_map):
    """
    Tests whether ``ImageHandlerGroup.cg_get_image_weighted`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    image_handlers : ``list<ImageHandlerBase>``
        Image handlers to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    weight_map : `dict<int, float>`
        Weight map to prefer an image source over an other.
        
    Returns
    -------
    output : ``list<None | ImageDetailBase>``
    """
    image_handler = ImageHandlerGroup(*image_handlers)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = []
    async for image_detail in image_handler.cg_get_image_weighted(weight_map):
        vampytest.assert_instance(image_detail, ImageDetailBase, nullable = True)
        output.append(image_detail)
    
    return output


def _iter_options__is_character_filterable():
    image_handler_0 = ImageHandlerBase()
    image_handler_1 = ImageHandlerBase()
    
    image_detail_0 = ImageDetailStatic('https://orindance.party/')
    
    image_handler_2 = ImageHandlerStatic(
        PREFERRED_IMAGE_SOURCE_TOUHOU,
        [
            image_detail_0,
        ],
    )
    
    
    yield (
        [
            image_handler_0,
            image_handler_1,
        ],
        None,
        False,
    )
    
    
    yield (
        [
            image_handler_0,
            image_handler_2,
        ],
        None,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__is_character_filterable()).returning_last())
def test__ImageHandlerGroup__is_character_filterable(image_handlers, attributes_to_set):
    """
    Tests whether ``ImageHandlerGroup.is_character_filterable`` works as intended.
    
    Parameters
    ----------
    image_handlers : ``list<ImageHandlerBase>``
        Image handlers to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    Returns
    -------
    output : `bool`
    """
    image_handler = ImageHandlerGroup(*image_handlers)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = image_handler.is_character_filterable()
    
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__iter_character_filterable():
    image_handler_0 = ImageHandlerBase()
    image_handler_1 = ImageHandlerBase()
    
    image_detail_0 = ImageDetailStatic('https://orindance.party/')
    
    image_handler_2 = ImageHandlerStatic(
        PREFERRED_IMAGE_SOURCE_TOUHOU,
        [
            image_detail_0,
        ],
    )
    
    
    yield (
        [
            image_handler_0,
            image_handler_1,
        ],
        None,
        [],
    )
    
    
    yield (
        [
            image_handler_0,
            image_handler_2,
        ],
        None,
        [
            image_detail_0,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_character_filterable()).returning_last())
def test__ImageHandlerGroup__iter_character_filterable(image_handlers, attributes_to_set):
    """
    Tests whether ``ImageHandlerGroup.iter_character_filterable`` works as intended.
    
    Parameters
    ----------
    image_handlers : ``list<ImageHandlerBase>``
        Image handlers to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    Returns
    -------
    output : ``list<ImageDetailBase>``
    """
    image_handler = ImageHandlerGroup(*image_handlers)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = [*image_handler.iter_character_filterable()]
    
    for element in output:
        vampytest.assert_instance(element, ImageDetailBase)
    
    return output

def _iter_options__supports_weight_mapping():
    image_handler_0 = ImageHandlerBase()
    image_handler_1 = ImageHandlerBase()
    
    image_detail_0 = ImageDetailStatic('https://orindance.party/')
    
    image_handler_2 = ImageHandlerStatic(
        PREFERRED_IMAGE_SOURCE_TOUHOU,
        [
            image_detail_0,
        ],
    )
    
    yield (
        [
            image_handler_0,
            image_handler_1,
        ],
        None,
        False,
    )
    
    
    yield (
        [
            image_handler_0,
            image_handler_2,
        ],
        None,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__supports_weight_mapping()).returning_last())
def test__ImageHandlerGroup__supports_weight_mapping(image_handlers, attributes_to_set):
    """
    Tests whether ``ImageHandlerGroup.supports_weight_mapping`` works as intended.
    
    Parameters
    ----------
    image_handlers : ``list<ImageHandlerBase>``
        Image handlers to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    Returns
    -------
    output : `int`
    """
    image_handler = ImageHandlerGroup(*image_handlers)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = image_handler.supports_weight_mapping()
    
    vampytest.assert_instance(output, bool)
    
    return output
