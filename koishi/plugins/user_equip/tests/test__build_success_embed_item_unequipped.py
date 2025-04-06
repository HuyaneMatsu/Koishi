import vampytest
from hata import Embed

from ...item_core import ITEM_FLAG_HEAD, ITEM_ID_PEACH, get_item

from ..embed_builders import build_success_embed_item_unequipped 


def _iter_options():
    item = get_item(ITEM_ID_PEACH)
    yield (
        ITEM_FLAG_HEAD,
        item,
        Embed(
            'Great success!',
            f'You unequipped your head accessory, {item.name}.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_item_unequipped(item_flag, item):
    """
    Tests whether ``build_success_embed_item_unequipped`` works as intended.
    
    Parameters
    ----------
    item_flag : `int`
        The item flag to filter for.
    
    item : ``Item``
        The unequipped item.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed_item_unequipped(item_flag, item)
    vampytest.assert_instance(output, Embed)
    return output
