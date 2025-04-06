import vampytest
from hata import Embed

from ...item_core import ITEM_FLAG_HEAD, ITEM_ID_PEACH, ITEM_ID_STRAWBERRY, get_item

from ..embed_builders import build_success_embed_item_replaced 


def _iter_options():
    old_item = get_item(ITEM_ID_PEACH)
    new_item = get_item(ITEM_ID_STRAWBERRY)
    yield (
        ITEM_FLAG_HEAD,
        old_item,
        new_item,
        Embed(
            'Great success!',
            f'You equipped {new_item.name} as your head accessory, unequipping {old_item.name}.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_item_replaced(item_flag, old_item, new_item):
    """
    Tests whether ``build_success_embed_item_replaced`` works as intended.
    
    Parameters
    ----------
    item_flag : `int`
        The item flag to filter for.
    
    old_item : ``Item``
        The removed item.
    
    new_item : ``Item``
        The selected item.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed_item_replaced(item_flag, old_item, new_item)
    vampytest.assert_instance(output, Embed)
    return output
