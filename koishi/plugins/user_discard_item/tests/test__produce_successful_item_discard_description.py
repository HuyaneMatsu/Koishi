import vampytest

from ...item_core import ITEM_ID_FISHING_ROD, get_item

from ..content_building import produce_successful_item_discard_description 


def _iter_options():
    item = get_item(ITEM_ID_FISHING_ROD)
    
    yield (
        item,
        56,
        0,
        f'You discarded 56 {item.emoji} {item.name}.',
    )
    
    yield (
        item,
        56,
        12,
        f'You discarded 56 {item.emoji} {item.name}, keeping 12.',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_successful_item_discard_description(item, discarded_amount, new_amount):
    """
    Tests whether ``produce_successful_item_discard_description`` works as intended.
    
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
    output : `str`
    """
    output = [*produce_successful_item_discard_description(item, discarded_amount, new_amount)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
