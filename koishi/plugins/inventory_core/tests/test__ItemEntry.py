import vampytest

from ...item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY, Item, get_item

from ..item_entry import ItemEntry


def _assert_fields_set(item_entry):
    """
    Tests whether the item entry has all of its fields set.
    """
    vampytest.assert_instance(item_entry, ItemEntry)
    vampytest.assert_instance(item_entry.amount, int)
    vampytest.assert_instance(item_entry.entry_id, int)
    vampytest.assert_instance(item_entry.item, Item)


def test__ItemEntry__new():
    """
    Tests whether ``ItemEntry.__new__`` works as intended.
    """
    item = get_item(ITEM_ID_PEACH)
    amount = 4
    
    item_entry = ItemEntry(item, amount)
    _assert_fields_set(item_entry)
    
    vampytest.assert_eq(item_entry.amount, amount)
    vampytest.assert_is(item_entry.item, item)
    vampytest.assert_eq(item_entry.entry_id, 0)


def test__ItemEntry__repr():
    """
    Tests whether ``ItemEntry.__repr__`` works as intended.
    """
    item = get_item(ITEM_ID_PEACH)
    amount = 4
    
    item_entry = ItemEntry(item, amount)
    
    output = repr(item_entry)
    vampytest.assert_instance(output, str)


def test__ItemEntry__from_entry():
    """
    Tests whether ``ItemEntry.from_entry`` works as intended.
    """
    item = get_item(ITEM_ID_PEACH)
    amount = 4
    entry_id = 6
    
    entry = {
        'amount': amount,
        'id': entry_id,
        'item_id': item.id,
    }
    item_entry = ItemEntry.from_entry(entry)
    _assert_fields_set(item_entry)
    
    vampytest.assert_eq(item_entry.amount, amount)
    vampytest.assert_eq(item_entry.entry_id, entry_id)
    vampytest.assert_is(item_entry.item, item)


def test__ItemEntry__copy():
    """
    Tests whether ``ItemEntry.__new__`` works as intended.
    """
    item = get_item(ITEM_ID_PEACH)
    amount = 4
    entry_id = 5
    
    item_entry = ItemEntry(item, amount)
    item_entry.entry_id = entry_id
    
    copy = item_entry.copy()
    vampytest.assert_instance(copy, ItemEntry)
    _assert_fields_set(copy)
    
    vampytest.assert_eq(copy.amount, amount)
    vampytest.assert_is(copy.item, item)
    vampytest.assert_eq(copy.entry_id, entry_id)



def _iter_options__eq():
    yield (
        get_item(ITEM_ID_PEACH),
        5,
        get_item(ITEM_ID_PEACH),
        5,
        True,
    )
    
    yield (
        get_item(ITEM_ID_PEACH),
        5,
        get_item(ITEM_ID_PEACH),
        4,
        False,
    )
    
    yield (
        get_item(ITEM_ID_PEACH),
        5,
        get_item(ITEM_ID_STRAWBERRY),
        5,
        False,
    )
    

@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ItemEntry__eq(item_0, amount_0, item_1, amount_1):
    """
    Tests whether ``ItemEntry.__eq__`` works as intended.
    
    Parameters
    ----------
    item_0 : ``Item``
        Item to create instance with.
    
    amount_0 : `int`
        Amount to create instance with.
    
    item_1 : ``Item``
        Item to create instance with.
    
    amount_1 : `int`
        Amount to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    instance_0 = ItemEntry(item_0, amount_0)
    instance_1 = ItemEntry(item_1, amount_1)
    
    output = instance_0 == instance_1
    vampytest.assert_instance(output, bool)
    return output


def test__ItemEntry__hash():
    """
    Tests whether ``ItemEntry.__hash__`` works as intended.
    """
    item = get_item(ITEM_ID_PEACH)
    amount = 4
    
    item_entry = ItemEntry(item, amount)
    
    output = hash(item_entry)
    vampytest.assert_instance(output, int)

