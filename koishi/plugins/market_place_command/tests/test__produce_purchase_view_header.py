import vampytest

from ...item_core import ITEM_FLAG_EDIBLE, ITEM_ID_PEACH, get_item

from ..content_building import produce_purchase_view_header


def _iter_options():
    item = get_item(ITEM_ID_PEACH)
    
    yield (
        None,
        0,
        2,
        (
            f'# Market place\n'
            f'Page: 3'
        ),
    )
    
    yield (
        item,
        0,
        2,
        (
            f'# Market place\n'
            f'Page: 3; filtered for item: {item.emoji} {item.name}'
        ),
    )
    
    yield (
        None,
        ITEM_FLAG_EDIBLE,
        2,
        (
            f'# Market place\n'
            f'Page: 3; filtered for category: edible'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_purchase_view_header(item, required_flags, page_index):
    """
    Tests whether ``produce_purchase_view_header`` works as intended.
    
    Parameters
    ----------
    item : ``None | Item``
        Item the user is filtering for.
    
    required_flags : `int`
        Item flags the user is filtering for.
    
    page_index : `int`
        The page's index.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_purchase_view_header(item, required_flags, page_index)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
