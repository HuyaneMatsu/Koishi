import vampytest

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
    vampytest.assert_instance(farewell_style.client_id, int)
    vampytest.assert_instance(farewell_style.items, tuple)
    vampytest.assert_instance(farewell_style.name, str)


def test__FarewellStyle__new():
    """
    Tests whether ``FarewellStyle.__new__`` works as intended.
    """
    name = 'koishi'
    client_id = 202502080010
    items = (
        FarewellStyleItem(
            (lambda target: 'content'),
            'image.png',
            'miau',
        ),
    )
    
    farewell_style = FarewellStyle(
        name,
        client_id,
        items,
    )
    _assert_fields_set(farewell_style)
    
    vampytest.assert_eq(farewell_style.client_id, client_id)
    vampytest.assert_eq(farewell_style.items, items)
    vampytest.assert_eq(farewell_style.name, name)


def test__FarewellStyle__repr():
    """
    Tests whether ``FarewellStyle.__repr__`` works as intended.
    """
    name = 'koishi'
    client_id = 202502080011
    items = (
        FarewellStyleItem(
            (lambda target: 'content'),
            'image.png',
            'miau',
        ),
    )
    
    farewell_style = FarewellStyle(
        name,
        client_id,
        items,
    )
    
    vampytest.assert_instance(repr(farewell_style), str)
