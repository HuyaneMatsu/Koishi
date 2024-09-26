from types import FunctionType

import vampytest
from hata import Locale

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
    vampytest.assert_instance(farewell_style_item.message_content_builder_localizations, dict, nullable = True)


def test__FarewellStyleItem__new():
    """
    Tests whether ``FarewellStyleItem.__new__`` works as intended.
    """
    image = 'image.png'
    image_creator = 'remilia'
    message_content_builder = lambda target: 'content'
    message_content_builder_localizations = {
        Locale.spanish: lambda target: 'content miau'
    }
    
    farewell_style_item = FarewellStyleItem(
        image,
        image_creator,
        message_content_builder,
        message_content_builder_localizations,
    )
    _assert_fields_set(farewell_style_item)
    vampytest.assert_eq(farewell_style_item.image, image)
    vampytest.assert_is(farewell_style_item.image_creator, image_creator)
    vampytest.assert_is(farewell_style_item.message_content_builder, message_content_builder)
    vampytest.assert_eq(farewell_style_item.message_content_builder_localizations, message_content_builder_localizations)


def test__FarewellStyleItem__repr():
    """
    Tests whether ``FarewellStyleItem.__repr__`` works as intended.
    """
    image = 'image.png'
    image_creator = 'remilia'
    message_content_builder = lambda target: 'content'
    message_content_builder_localizations = {
        Locale.spanish: lambda target: 'content miau'
    }
    
    farewell_style_item = FarewellStyleItem(
        image,
        image_creator,
        message_content_builder,
        message_content_builder_localizations,
    )
    
    vampytest.assert_instance(repr(farewell_style_item), str)


def test__FarewellStyleItem__get_message_content_builder_localized__no_localization():
    """
    Tests whether ``FarewellStyleItem.get_message_content_builder_localized`` works as intended.
    
    Case: No localization.
    """
    image = 'image.png'
    image_creator = 'remilia'
    message_content_builder = lambda target: 'content'
    
    farewell_style_item = FarewellStyleItem(
        image,
        image_creator,
        message_content_builder,
    )
    
    output = farewell_style_item.get_message_content_builder_localized(Locale.spanish)
    vampytest.assert_is(output, message_content_builder)


def test__FarewellStyleItem__get_message_content_builder_localized__miss_localization():
    """
    Tests whether ``FarewellStyleItem.get_message_content_builder_localized`` works as intended.
    
    Case: Miss localization.
    """
    image = 'image.png'
    image_creator = 'remilia'
    message_content_builder = lambda target: 'content'
    message_content_builder_finnish = lambda target: 'content miau'
    
    farewell_style_item = FarewellStyleItem(
        image,
        image_creator,
        message_content_builder,
        {
            Locale.finnish: message_content_builder_finnish,
        },
    )
    
    output = farewell_style_item.get_message_content_builder_localized(Locale.spanish)
    vampytest.assert_is(output, message_content_builder)


def test__FarewellStyleItem__get_message_content_builder_localized__hit_localization():
    """
    Tests whether ``FarewellStyleItem.get_message_content_builder_localized`` works as intended.
    
    Case: Hit localization.
    """
    image = 'image.png'
    image_creator = 'remilia'
    message_content_builder = lambda target: 'content'
    message_content_builder_spanish = lambda target: 'content miau'
    
    farewell_style_item = FarewellStyleItem(
        image,
        image_creator,
        message_content_builder,
        {
            Locale.spanish: message_content_builder_spanish,
        },
    )
    
    output = farewell_style_item.get_message_content_builder_localized(Locale.spanish)
    vampytest.assert_is(output, message_content_builder_spanish)
