import vampytest

from ..constants import PAGE_SIZE
from ..helpers import get_next_page_index


def _iter_options():
    yield (
        0,
        0,
        False,
        0,
    )
    
    yield (
        0,
        1 * PAGE_SIZE,
        False,
        0,
    )
    
    yield (
        0,
        2 * PAGE_SIZE,
        False,
        1,
    )
    
    yield (
        1,
        2 * PAGE_SIZE,
        False,
        0,
    )
    
    # Test some random order as well, although not giving it real random choices.
    yield (
        0,
        0,
        True,
        0,
    )
    
    yield (
        0,
        1 * PAGE_SIZE,
        True,
        0,
    )
    
    yield (
        0,
        2 * PAGE_SIZE,
        True,
        1,
    )
    
    yield (
        1,
        2 * PAGE_SIZE,
        True,
        0,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_next_page_index(current_page, total_entry_count, random_order):
    """
    Tests whether ``get_next_page_index`` works as intended.
    
    Parameters
    ----------
    current_page : `int`
        The current page's index.
    
    total_entry_count : `int`
        The total amount of entries.
    
    random_order : `bool`
        Whether images should be shown in random order.
    
    Returns
    -------
    output : `int`
    """
    output = get_next_page_index(current_page, total_entry_count, random_order)
    vampytest.assert_instance(output, int)
    return output
