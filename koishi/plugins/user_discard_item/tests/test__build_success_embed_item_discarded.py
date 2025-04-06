import vampytest
from hata import Embed

from ...item_core import ITEM_ID_FISHING_ROD, get_item

from ..embed_builders import build_success_embed_item_discarded 


def _iter_options():
    item = get_item(ITEM_ID_FISHING_ROD)
    
    yield (
        item,
        56,
        0,
        Embed(
            'Great success!',
            f'You discarded 56 {item.name}.',
        ),
    )
    
    yield (
        item,
        56,
        12,
        Embed(
            'Great success!',
            f'You discarded 56 {item.name}, keeping 12.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_item_discarded(item, discarded_amount, new_amount):
    """
    Tests whether ``build_success_embed_item_discarded`` works as intended.
    
    Parameters
    ----------
    item : ``Item``
        The selected item.
    
    discarded_amount : `int`
        The amount of cards discarded.
    
    new_amount : `int`
        Items left.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed_item_discarded(item, discarded_amount, new_amount)
    vampytest.assert_instance(output, Embed)
    return output
