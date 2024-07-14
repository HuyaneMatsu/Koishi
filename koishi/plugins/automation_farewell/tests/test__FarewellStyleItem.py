from types import FunctionType

import vampytest

from ..farewell_style_item import FarewellStyleItem


def _assert_fields_set(farewell_style_item):
    """
    Asserts whether every fields are set of the given farewell style item.
    
    Parameters
    ----------
    farewell_style_item : ``FarewellStyleItem``
        The reply style to test.
    """
    vampytest.assert_instance(farewell_style_item, FarewellStyleItem)
    vampytest.assert_instance(farewell_style_item.image, str)
    vampytest.assert_instance(farewell_style_item.image_creator, str)
    vampytest.assert_instance(farewell_style_item.message_content_builder, FunctionType)


def test__FarewellStyleItem__new():
    """
    Tests whether ``FarewellStyleItem.__new__`` works as intended.
    """
    image = 'image.png'
    image_creator = 'remilia'
    message_content_builder = lambda target: 'content'
    
    farewell_style_item = FarewellStyleItem(message_content_builder, image, image_creator)
    _assert_fields_set(farewell_style_item)
    vampytest.assert_eq(farewell_style_item.image, image)
    vampytest.assert_is(farewell_style_item.image_creator, image_creator)
    vampytest.assert_is(farewell_style_item.message_content_builder, message_content_builder)


def test__FarewellStyleItem__repr():
    """
    Tests whether ``FarewellStyleItem.__repr__`` works as intended.
    """
    image = 'image.png'
    image_creator = 'remilia'
    message_content_builder = lambda target: 'content'
    
    farewell_style_item = FarewellStyleItem(message_content_builder, image, image_creator)
    
    vampytest.assert_instance(repr(farewell_style_item), str)
