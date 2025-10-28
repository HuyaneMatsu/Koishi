import vampytest

from ....image_commands_actions.asset_listings.constants import ACTION_TAG_FEED
from ....touhou_core import KOMEIJI_KOISHI, KOMEIJI_SATORI
from ....user_settings import PREFERRED_IMAGE_SOURCE_NONE, PREFERRED_IMAGE_SOURCE_TOUHOU

from ...image_detail import ImageDetailBase, ImageDetailStatic

from ..static import ImageHandlerStatic


def _assert_fields_set(image_handler):
    """
    Asserts whether every fields are set of the given image handler.
    
    Parameters
    ----------
    image_handler : ``ImageHandlerStatic``
        The image handler to check.
    """
    vampytest.assert_instance(image_handler, ImageHandlerStatic)
    vampytest.assert_instance(image_handler._images, list)
    vampytest.assert_instance(image_handler._source, int)


def test__ImageHandlerStatic__new():
    """
    Asserts whether ``ImageHandlerStatic.__new__`` works as intended.
    """
    source = PREFERRED_IMAGE_SOURCE_TOUHOU
    image_detail_0 = ImageDetailStatic('https://orindance.party/')
    
    image_handler = ImageHandlerStatic(source, [image_detail_0])
    _assert_fields_set(image_handler)
    
    vampytest.assert_eq(image_handler._images, [image_detail_0])
    vampytest.assert_eq(image_handler._source, source)
    

def _iter_options__eq():
    image_detail_0 = ImageDetailStatic('https://orindance.party/')
    
    keyword_parameters = {
        'source': PREFERRED_IMAGE_SOURCE_TOUHOU,
        'images': [image_detail_0],
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
            'source': PREFERRED_IMAGE_SOURCE_NONE,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'images': [],
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ImageHandlerStatic__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ImageHandlerStatic.__eq__`` works as intended.
    
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
    image_handler_0 = ImageHandlerStatic(**keyword_parameters_0)
    image_handler_1 = ImageHandlerStatic(**keyword_parameters_1)
    
    output = image_handler_0 == image_handler_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__cg_get_image():
    image_detail_0 = ImageDetailStatic('https://orindance.party/')
    
    yield (
        {
            'source': PREFERRED_IMAGE_SOURCE_TOUHOU,
            'images': [],
        },
        None,
        [],
    )
    
    yield (
        {
            'source': PREFERRED_IMAGE_SOURCE_TOUHOU,
            'images': [image_detail_0],
        },
        None,
        [image_detail_0],
    )


@vampytest._(vampytest.call_from(_iter_options__cg_get_image()).returning_last())
async def test__ImageHandlerStatic__cg_get_image(keyword_parameters, attributes_to_set):
    """
    Tests whether ``ImageHandlerStatic.cg_get_image`` works as intended.
    
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
    image_handler = ImageHandlerStatic(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = []
    async for image_detail in image_handler.cg_get_image():
        vampytest.assert_instance(image_detail, ImageDetailBase, nullable = True)
        output.append(image_detail)
    
    return output


def _iter_options__get_weight():
    image_detail_0 = ImageDetailStatic('https://orindance.party/')
    
    yield (
        {
            'source': PREFERRED_IMAGE_SOURCE_TOUHOU,
            'images': [],
        },
        None,
        0.0,
    )
    
    yield (
        {
            'source': PREFERRED_IMAGE_SOURCE_TOUHOU,
            'images': [image_detail_0],
        },
        None,
        0.01,
    )


@vampytest._(vampytest.call_from(_iter_options__get_weight()).returning_last())
def test__ImageHandlerStatic__get_weight(keyword_parameters, attributes_to_set):
    """
    Tests whether ``ImageHandlerStatic.get_weight`` works as intended.
    
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
    image_handler = ImageHandlerStatic(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = image_handler.get_weight()
    
    vampytest.assert_instance(output, float)
    return output


def _iter_options__is_character_filterable():
    image_detail_0 = ImageDetailStatic('https://orindance.party/')
    
    yield (
        {
            'source': PREFERRED_IMAGE_SOURCE_TOUHOU,
            'images': [image_detail_0],
        },
        None,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__is_character_filterable()).returning_last())
def test__ImageHandlerStatic__is_character_filterable(keyword_parameters, attributes_to_set):
    """
    Tests whether ``ImageHandlerStatic.is_character_filterable`` works as intended.
    
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
    image_handler = ImageHandlerStatic(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = image_handler.is_character_filterable()
    
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__iter_character_filterable():
    image_detail_0 = ImageDetailStatic('https://orindance.party/')
    
    yield (
        {
            'source': PREFERRED_IMAGE_SOURCE_TOUHOU,
            'images': [image_detail_0],
        },
        None,
        [image_detail_0],
    )
    
    yield (
        {
            'source': PREFERRED_IMAGE_SOURCE_TOUHOU,
            'images': [],
        },
        None,
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_character_filterable()).returning_last())
def test__ImageHandlerStatic__iter_character_filterable(keyword_parameters, attributes_to_set):
    """
    Tests whether ``ImageHandlerStatic.iter_character_filterable`` works as intended.
    
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
    image_handler = ImageHandlerStatic(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = [*image_handler.iter_character_filterable()]
    
    for element in output:
        vampytest.assert_instance(element, ImageDetailBase)
    
    return output


def _iter_options__get_image_source():
    image_detail_0 = ImageDetailStatic('https://orindance.party/')
    
    yield (
        {
            'source': PREFERRED_IMAGE_SOURCE_TOUHOU,
            'images': [image_detail_0],
        },
        None,
        PREFERRED_IMAGE_SOURCE_TOUHOU,
    )
    
    yield (
        {
            'source': PREFERRED_IMAGE_SOURCE_NONE,
            'images': [image_detail_0],
        },
        None,
        PREFERRED_IMAGE_SOURCE_NONE,
    )


@vampytest._(vampytest.call_from(_iter_options__get_image_source()).returning_last())
def test__ImageHandlerStatic__get_image_source(keyword_parameters, attributes_to_set):
    """
    Tests whether ``ImageHandlerStatic.get_image_source`` works as intended.
    
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
    image_handler = ImageHandlerStatic(**keyword_parameters)
    
    if (attributes_to_set is not None):
        for item in attributes_to_set:
            setattr(image_handler, *item)
    
    output = image_handler.get_image_source()
    
    vampytest.assert_instance(output, int)
    
    return output


def test__ImageHandlerStatic__add():
    """
    Tests whether ``ImageHandlerStatic.add`` works as intended.
    """
    image_handler = ImageHandlerStatic(PREFERRED_IMAGE_SOURCE_TOUHOU, [])
    
    url = 'https://orindance.party/'
    
    output = image_handler.add(url)
    vampytest.assert_instance(output, ImageDetailStatic)
    vampytest.assert_eq(output.url, url)
    vampytest.assert_eq(image_handler._images, [output])
    

def test__ImageHandlerStatic__create_action_subset():
    """
    Tests whether ``ImageHandlerStatic.create_action_subset`` works as intended.
    """
    source = PREFERRED_IMAGE_SOURCE_TOUHOU
    
    image_detail_0 = ImageDetailStatic(
        'https://orindance.party/'
    )
    image_detail_1 = ImageDetailStatic(
        'https://orindance.party/'
    ).with_action(
        ACTION_TAG_FEED, KOMEIJI_KOISHI, KOMEIJI_SATORI,
    )
    
    image_handler = ImageHandlerStatic(
        source,
        [
            image_detail_0,
            image_detail_1,
        ],
    )
    
    output = image_handler.create_action_subset(ACTION_TAG_FEED)
    _assert_fields_set(output)
    vampytest.assert_eq(output._source, source)
    vampytest.assert_eq(output._images, [image_detail_1])
