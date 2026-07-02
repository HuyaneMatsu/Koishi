import vampytest

from ..flags import ITEM_FLAG_BUTCHERABLE
from ..item import Item
from ..logic_butcher import butcher_get_part_count
from ..option_butcher import OptionButcher


def _iter_options():
    item_id_0 = 8
    item_id_1 = 9
    item_id_2 = 10
    item_id_3 = 11
    
    item_0 = Item(
        item_id_0,
        'item 0',
        None,
        'description',
        ITEM_FLAG_BUTCHERABLE,
        0,
        0,
        None,
        (
            OptionButcher(False, 1, 2, 2, item_id_1, 0, 10, 0),
            OptionButcher(False, 1, 2, 2, item_id_3, 0, 2, 0),
        ),
    )
    
    item_1 = Item(
        item_id_1,
        'item 1',
        None,
        'description',
        ITEM_FLAG_BUTCHERABLE,
        0,
        0,
        None,
        (
            OptionButcher(True, 1, 2, 2, item_id_2, 0, 5, 0),
            OptionButcher(True, 1, 2, 2, item_id_3, 0, 3, 0),
        ),
    )
    
    item_2 = Item(
        item_id_2,
        'item 2',
        None,
        'description',
        ITEM_FLAG_BUTCHERABLE,
        0,
        0,
        None,
        (
            OptionButcher(True, 1, 2, 10, item_id_3, 0, 1, 0),
        ),
    )
    
    item_3 = Item(
        item_id_3,
        'item 3',
        None,
        'description',
        0,
        0,
        0,
        None,
        None,
    )
    
    items = {
        item_id_0 : item_0,
        item_id_1 : item_1,
        item_id_2 : item_2,
        item_id_3 : item_3,
    }
    
    yield (
        item_0,
        items,
        6,
    )
    
    yield (
        item_1,
        items,
        2,
    )
    
    yield (
        item_2,
        items,
        0,
    )
    
    yield (
        item_3,
        items,
        0,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__butcher_get_part_count(item, items):
    """
    Tests whether ``butcher_get_part_count`` works as intended.
    
    Parameters
    ----------
    item : ``Item``
        Item to butcher.
    
    items : ``dict<int, Item>``
        Items to work with.
    
    Returns
    -------
    output : `int`
    """
    mocked = vampytest.mock_globals(
        butcher_get_part_count,
        2,
        ITEMS = items,
    )
    
    output = mocked(item)
    vampytest.assert_instance(output, int)
    return output
