import vampytest
from hata import Embed

from ...item_core import ITEM_ID_FISHING_ROD, get_item

from ..embed_builders import build_failure_embed_no_item_discarded 


def _iter_options():
    item = get_item(ITEM_ID_FISHING_ROD)
    
    yield (
        item,
        56,
        Embed(
            'Oh no',
            f'You did not discard any of your 56 {item.name}.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_no_item_discarded(item, new_amount):
    """
    Tests whether ``build_failure_embed_no_item_discarded`` works as intended.
    
    Parameters
    ----------
    item : ``Item``
        The selected item.
    
    new_amount : `int`
        Items left.
    
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_no_item_discarded(item, new_amount)
    vampytest.assert_instance(output, Embed)
    return output
