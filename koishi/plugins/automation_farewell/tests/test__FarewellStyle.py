import vampytest
from hata import BUILTIN_EMOJIS

from ..farewell_style_item import FarewellStyleItem
from ..farewell_style import FarewellStyle


def _assert_fields_set(farewell_style):
    """
    Asserts whether every attributes of the farewell style are set.
    
    Parameters
    ----------
    farewell_style : ``FarewellStyle``
        The farewell style to check.
    """
    vampytest.assert_instance(farewell_style, FarewellStyle)
    vampytest.assert_instance(farewell_style.items, tuple)
    vampytest.assert_instance(farewell_style.name, str)


def test__FarewellStyle__new():
    """
    Tests whether ``FarewellStyle.__new__`` works as intended.
    """
    name = 'koishi'
    items = (
        FarewellStyleItem(
            (lambda target: 'content'),
            'image.png',
            'miau',
        ),
    )
    
    farewell_style = FarewellStyle(
        name,
        items,
    )
    _assert_fields_set(farewell_style)
    
    vampytest.assert_eq(farewell_style.items, items)
    vampytest.assert_eq(farewell_style.name, name)


def test__FarewellStyle__repr():
    """
    Tests whether ``FarewellStyle.__repr__`` works as intended.
    """
    name = 'koishi'
    items = (
        FarewellStyleItem(
            (lambda target: 'content'),
            'image.png',
            'miau',
        ),
    )
    
    farewell_style = FarewellStyle(
        name,
        items,
    )
    
    vampytest.assert_instance(repr(farewell_style), str)
