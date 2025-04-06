import vampytest
from hata import Embed

from ...item_core import ITEM_FLAG_HEAD, ITEM_ID_PEACH, get_item

from ..embed_builders import build_failure_embed_same_item 


def _iter_options():
    item = get_item(ITEM_ID_PEACH)
    yield (
        ITEM_FLAG_HEAD,
        item,
        Embed(
            'Oh no',
            f'Are you sure you do not have {item.name} already equipped as head accessory?',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_same_item(item_flag, item):
    """
    Tests whether ``build_failure_embed_same_item`` works as intended.
    
    Parameters
    ----------
    item_flag : `int`
        The item flag to filter for.
    
    item : ``Item``
        The selected item.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_same_item(item_flag, item)
    vampytest.assert_instance(output, Embed)
    return output
