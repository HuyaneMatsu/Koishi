import vampytest

from ....user_settings import PREFERRED_IMAGE_SOURCE_NONE

from ...image_detail import ImageDetailBase

from ..base import ImageHandlerBase


def _assert_fields_set(image_handler):
    """
    Asserts whether every fields are set of the given image handler.
    
    Parameters
    ----------
    image_handler : ``ImageHandlerBase``
        The image handler to check.
    """
    vampytest.assert_instance(image_handler, ImageHandlerBase)


def test__ImageHandlerBase__new():
    """
    Asserts whether ``ImageHandlerBase.__new__`` works as intended.
    """
    image_handler = ImageHandlerBase()
    _assert_fields_set(image_handler)


def _iter_options__eq():
    keyword_parameters = {}
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ImageHandlerBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ImageHandlerBase.__eq__`` works as intended.
    
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
    image_handler_0 = ImageHandlerBase(**keyword_parameters_0)
    image_handler_1 = ImageHandlerBase(**keyword_parameters_1)
    
    output = image_handler_0 == image_handler_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__cg_get_image():
    yield (
        {},
        None,
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__cg_get_image()).returning_last())
async def test__ImageHandlerBase__cg_get_image(keyword_parameters, attributes_to_set):
    """
    Tests whether ``ImageHandlerBase.cg_get_image`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    Returns
    -------
    output : ``list<None | ImageDetailBase>``
    """
    image_handler = ImageHandlerBase(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = []
    async for image_detail in image_handler.cg_get_image():
        vampytest.assert_instance(image_detail, ImageDetailBase, nullable = True)
        output.append(image_detail)
    
    return output


def _iter_options__cg_get_image_weighted():
    yield (
        {},
        None,
        {
            PREFERRED_IMAGE_SOURCE_NONE : 1.0,
        },
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__cg_get_image_weighted()).returning_last())
async def test__ImageHandlerBase__cg_get_image_weighted__no_cache(keyword_parameters, attributes_to_set, weight_map):
    """
    Tests whether ``ImageHandlerBase.cg_get_image_weighted`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    weight_map : `dict<int, float>`
        Weight map to prefer an image source over an other.
        
    Returns
    -------
    output : ``list<None | ImageDetailBase>``
    """
    image_handler = ImageHandlerBase(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = []
    async for image_detail in image_handler.cg_get_image_weighted(weight_map):
        vampytest.assert_instance(image_detail, ImageDetailBase, nullable = True)
        output.append(image_detail)
    
    return output


def _iter_options__get_weight():
    yield (
        {},
        None,
        1.0,
    )


@vampytest._(vampytest.call_from(_iter_options__get_weight()).returning_last())
def test__ImageHandlerBase__get_weight(keyword_parameters, attributes_to_set):
    """
    Tests whether ``ImageHandlerBase.get_weight`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    Returns
    -------
    output : `float`
    """
    image_handler = ImageHandlerBase(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = image_handler.get_weight()
    
    vampytest.assert_instance(output, float)
    return output


def _iter_options__is_character_filterable():
    yield (
        {},
        None,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__is_character_filterable()).returning_last())
def test__ImageHandlerBase__is_character_filterable(keyword_parameters, attributes_to_set):
    """
    Tests whether ``ImageHandlerBase.is_character_filterable`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    Returns
    -------
    output : `bool`
    """
    image_handler = ImageHandlerBase(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = image_handler.is_character_filterable()
    
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__iter_character_filterable():
    yield (
        {},
        None,
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_character_filterable()).returning_last())
def test__ImageHandlerBase__iter_character_filterable(keyword_parameters, attributes_to_set):
    """
    Tests whether ``ImageHandlerBase.iter_character_filterable`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    Returns
    -------
    output : ``list<ImageDetailBase>``
    """
    image_handler = ImageHandlerBase(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = [*image_handler.iter_character_filterable()]
    
    for element in output:
        vampytest.assert_instance(element, ImageDetailBase)
    
    return output


def _iter_options__get_image_source():
    yield (
        {},
        None,
        PREFERRED_IMAGE_SOURCE_NONE,
    )


@vampytest._(vampytest.call_from(_iter_options__get_image_source()).returning_last())
def test__ImageHandlerBase__get_image_source(keyword_parameters, attributes_to_set):
    """
    Tests whether ``ImageHandlerBase.get_image_source`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    Returns
    -------
    output : `int`
    """
    image_handler = ImageHandlerBase(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = image_handler.get_image_source()
    
    vampytest.assert_instance(output, int)
    
    return output


def _iter_options__supports_weight_mapping():
    yield (
        {},
        None,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__supports_weight_mapping()).returning_last())
def test__ImageHandlerBase__supports_weight_mapping(keyword_parameters, attributes_to_set):
    """
    Tests whether ``ImageHandlerBase.supports_weight_mapping`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    attributes_to_set : `None | list<(str, object)>`
        Additional attributes to set of the created instance.
    
    Returns
    -------
    output : `int`
    """
    image_handler = ImageHandlerBase(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = image_handler.supports_weight_mapping()
    
    vampytest.assert_instance(output, bool)
    
    return output
