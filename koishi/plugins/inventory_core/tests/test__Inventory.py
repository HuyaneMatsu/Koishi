import vampytest

from ...item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY, get_item

from ..inventory import Inventory
from ..item_entry import ItemEntry


def _assert_fields_set(inventory):
    """
    Asserts whether the given inventory has all of its fields set.
    
    Parameters
    """
    vampytest.assert_instance(inventory, Inventory)
    vampytest.assert_instance(inventory.item_entries, dict, nullable = True)
    vampytest.assert_instance(inventory.item_entries_modified, dict, nullable = True)
    vampytest.assert_instance(inventory.user_id, int)
    vampytest.assert_instance(inventory.weight, int)


def test__Inventory__new():
    """
    Tests whether ``Inventory.__new__`` works as intended.
    """
    user_id = 202503270000
    
    inventory = Inventory(user_id)
    _assert_fields_set(inventory)
    
    vampytest.assert_eq(inventory.user_id, user_id)


def test__Inventory__repr():
    """
    Tests whether ``Inventory.__new__`` works as intended.
    """
    user_id = 202503270016
    entries = [
        {
            'id': 5,
            'item_id': ITEM_ID_PEACH,
            'amount': 4,
        },
    ]
    
    inventory = Inventory.from_entries(user_id, entries)
    inventory.modify_item_amount(get_item(ITEM_ID_STRAWBERRY), 5)
    
    output = repr(inventory)
    vampytest.assert_instance(output, str)


def test__Inventory__from_entries__empty():
    """
    Tests whether ``Inventory.from_entries`` works as intended.
    
    Case: Empty.
    """
    user_id = 202503270001
    entries = []
    
    inventory = Inventory.from_entries(user_id, entries)
    _assert_fields_set(inventory)
    
    vampytest.assert_eq(inventory.user_id, user_id)
    vampytest.assert_is(inventory.item_entries, None)
    vampytest.assert_eq(inventory.weight, 0)
    
    
def test__Inventory__from_entries__with_items():
    """
    Tests whether ``Inventory.from_entries`` works as intended.
    
    Case: with items.
    """
    user_id = 202503270002
    entries = [
        {
            'id': 5,
            'item_id': ITEM_ID_PEACH,
            'amount': 4,
        },
        {
            'id': 6,
            'item_id': ITEM_ID_STRAWBERRY,
            'amount': 2,
        },
    ]
    
    inventory = Inventory.from_entries(user_id, entries)
    _assert_fields_set(inventory)
    
    vampytest.assert_eq(inventory.user_id, user_id)
    vampytest.assert_is_not(inventory.item_entries, None)
    vampytest.assert_eq(len(inventory.item_entries), 2)
    vampytest.assert_eq(inventory.item_entries.keys(), {ITEM_ID_PEACH, ITEM_ID_STRAWBERRY})
    vampytest.assert_eq(inventory.weight, get_item(ITEM_ID_PEACH).weight * 4 + get_item(ITEM_ID_STRAWBERRY).weight * 2)
    vampytest.assert_eq(inventory.item_entries[ITEM_ID_PEACH].amount, 4)
    vampytest.assert_eq(inventory.item_entries[ITEM_ID_STRAWBERRY].amount, 2)


def test__Inventory__modify_item_amount__remove_all_of_one():
    """
    Tests whether ``Inventory.modify_item_amount`` works as intended.
    
    Case: remove all of one.
    """
    user_id = 202503270003
    entries = [
        {
            'id': 5,
            'item_id': ITEM_ID_PEACH,
            'amount': 4,
        },
        {
            'id': 6,
            'item_id': ITEM_ID_STRAWBERRY,
            'amount': 2,
        },
    ]
    
    inventory = Inventory.from_entries(user_id, entries)
    
    output = inventory.modify_item_amount(get_item(ITEM_ID_PEACH), -4)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
    
    vampytest.assert_is_not(inventory.item_entries, None)
    vampytest.assert_eq(len(inventory.item_entries), 1)
    vampytest.assert_eq(inventory.item_entries.keys(), {ITEM_ID_STRAWBERRY})
    vampytest.assert_eq(inventory.item_entries[ITEM_ID_STRAWBERRY].amount, 2)
    
    vampytest.assert_is_not(inventory.item_entries_modified, None)
    vampytest.assert_eq(len(inventory.item_entries_modified), 1)
    vampytest.assert_eq(inventory.item_entries_modified.keys(), {ITEM_ID_PEACH})
    vampytest.assert_eq(inventory.item_entries_modified[ITEM_ID_PEACH].amount, 0)
    
    vampytest.assert_eq(inventory.weight, get_item(ITEM_ID_STRAWBERRY).weight * 2)


def test__Inventory__modify_item_amount__remove_some():
    """
    Tests whether ``Inventory.modify_item_amount`` works as intended.
    
    Case: remove some.
    """
    user_id = 202503270004
    entries = [
        {
            'id': 5,
            'item_id': ITEM_ID_PEACH,
            'amount': 4,
        },
        {
            'id': 6,
            'item_id': ITEM_ID_STRAWBERRY,
            'amount': 2,
        },
    ]
    
    inventory = Inventory.from_entries(user_id, entries)
    
    output = inventory.modify_item_amount(get_item(ITEM_ID_PEACH), -2)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)
    
    vampytest.assert_is_not(inventory.item_entries, None)
    vampytest.assert_eq(len(inventory.item_entries), 1)
    vampytest.assert_eq(inventory.item_entries.keys(), {ITEM_ID_STRAWBERRY})
    vampytest.assert_eq(inventory.item_entries[ITEM_ID_STRAWBERRY].amount, 2)
    
    vampytest.assert_is_not(inventory.item_entries_modified, None)
    vampytest.assert_eq(len(inventory.item_entries_modified), 1)
    vampytest.assert_eq(inventory.item_entries_modified.keys(), {ITEM_ID_PEACH})
    vampytest.assert_eq(inventory.item_entries_modified[ITEM_ID_PEACH].amount, 2)
    
    vampytest.assert_eq(inventory.weight, get_item(ITEM_ID_PEACH).weight * 2 + get_item(ITEM_ID_STRAWBERRY).weight * 2)


def test__Inventory__modify_item_amount__add_some():
    """
    Tests whether ``Inventory.modify_item_amount`` works as intended.
    
    Case: add some.
    """
    user_id = 202503270005
    entries = [
        {
            'id': 5,
            'item_id': ITEM_ID_PEACH,
            'amount': 4,
        },
        {
            'id': 6,
            'item_id': ITEM_ID_STRAWBERRY,
            'amount': 2,
        },
    ]
    
    inventory = Inventory.from_entries(user_id, entries)
    
    output = inventory.modify_item_amount(get_item(ITEM_ID_PEACH), +2)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 6)
    
    vampytest.assert_is_not(inventory.item_entries, None)
    vampytest.assert_eq(len(inventory.item_entries), 1)
    vampytest.assert_eq(inventory.item_entries.keys(), {ITEM_ID_STRAWBERRY})
    vampytest.assert_eq(inventory.item_entries[ITEM_ID_STRAWBERRY].amount, 2)
    
    vampytest.assert_is_not(inventory.item_entries_modified, None)
    vampytest.assert_eq(len(inventory.item_entries_modified), 1)
    vampytest.assert_eq(inventory.item_entries_modified.keys(), {ITEM_ID_PEACH})
    vampytest.assert_eq(inventory.item_entries_modified[ITEM_ID_PEACH].amount, 6)
    
    vampytest.assert_eq(inventory.weight, get_item(ITEM_ID_PEACH).weight * 6 + get_item(ITEM_ID_STRAWBERRY).weight * 2)


def test__Inventory__modify_item_amount__add_new():
    """
    Tests whether ``Inventory.modify_item_amount`` works as intended.
    
    Case: add some.
    """
    user_id = 202503270006
    entries = [
        {
            'id': 6,
            'item_id': ITEM_ID_STRAWBERRY,
            'amount': 2,
        },
    ]
    
    inventory = Inventory.from_entries(user_id, entries)
    
    output = inventory.modify_item_amount(get_item(ITEM_ID_PEACH), +2)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)
    
    vampytest.assert_is_not(inventory.item_entries, None)
    vampytest.assert_eq(len(inventory.item_entries), 1)
    vampytest.assert_eq(inventory.item_entries.keys(), {ITEM_ID_STRAWBERRY})
    vampytest.assert_eq(inventory.item_entries[ITEM_ID_STRAWBERRY].amount, 2)
    
    vampytest.assert_is_not(inventory.item_entries_modified, None)
    vampytest.assert_eq(len(inventory.item_entries_modified), 1)
    vampytest.assert_eq(inventory.item_entries_modified.keys(), {ITEM_ID_PEACH})
    vampytest.assert_eq(inventory.item_entries_modified[ITEM_ID_PEACH].amount, 2)
    
    vampytest.assert_eq(inventory.weight, get_item(ITEM_ID_PEACH).weight * 2 + get_item(ITEM_ID_STRAWBERRY).weight * 2)


def test__Inventory__modify_item_amount__double_modification():
    """
    Tests whether ``Inventory.modify_item_amount`` works as intended.
    
    Case: double modification.
    """
    user_id = 202503270007
    entries = [
        {
            'id': 6,
            'item_id': ITEM_ID_STRAWBERRY,
            'amount': 2,
        },
    ]
    
    inventory = Inventory.from_entries(user_id, entries)
    
    output = inventory.modify_item_amount(get_item(ITEM_ID_STRAWBERRY), +2)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 4)
    
    output = inventory.modify_item_amount(get_item(ITEM_ID_STRAWBERRY), +2)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 6)
    
    vampytest.assert_is(inventory.item_entries, None)
    
    vampytest.assert_is_not(inventory.item_entries_modified, None)
    vampytest.assert_eq(len(inventory.item_entries_modified), 1)
    vampytest.assert_eq(inventory.item_entries_modified.keys(), {ITEM_ID_STRAWBERRY})
    vampytest.assert_eq(inventory.item_entries_modified[ITEM_ID_STRAWBERRY].amount, 6)
    vampytest.assert_eq(inventory.item_entries_modified[ITEM_ID_STRAWBERRY].entry_id, 6)
    
    vampytest.assert_eq(inventory.weight, get_item(ITEM_ID_STRAWBERRY).weight * 6)


def test__Inventory__modify_item_amount__add_and_remove():
    """
    Tests whether ``Inventory.modify_item_amount`` works as intended.
    
    Case: add and remove.
    """
    user_id = 202503270011
    entries = []
    
    inventory = Inventory.from_entries(user_id, entries)
    
    output = inventory.modify_item_amount(get_item(ITEM_ID_STRAWBERRY), +2)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)
    
    output = inventory.modify_item_amount(get_item(ITEM_ID_STRAWBERRY), -2)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
    
    vampytest.assert_is(inventory.item_entries, None)
    vampytest.assert_is(inventory.item_entries_modified, None)
    
    vampytest.assert_eq(inventory.weight, 0)


def test__Inventory__get_modified_item_entry__none():
    """
    Tests whether ``Inventory.get_modified_item_entry`` works as intended.
    
    Case: none.
    """
    user_id = 202503270008
    entries = []
    
    inventory = Inventory.from_entries(user_id, entries)
    
    output = inventory.get_modified_item_entry()
    vampytest.assert_is(output, None)


def test__Inventory__get_modified_item_entry__has():
    """
    Tests whether ``Inventory.get_modified_item_entry`` works as intended.
    
    Case: none.
    """
    user_id = 202503270009
    entries = []
    
    inventory = Inventory.from_entries(user_id, entries)
    inventory.modify_item_amount(get_item(ITEM_ID_STRAWBERRY), +2)
    
    output = inventory.get_modified_item_entry()
    vampytest.assert_instance(output, ItemEntry)
    vampytest.assert_is(output.item, get_item(ITEM_ID_STRAWBERRY))
    vampytest.assert_is(output.amount, 2)


def test__Inventory__apply_modified_item_entry__no_modifications_and_zero():
    """
    Tests whether ``Inventory.apply_modified_item_entry`` works as intended.
    
    Case: no modifications & zero.
    """
    user_id = 202503270010
    entries = []
    amount = 0
    entry_id = 5
    
    inventory = Inventory.from_entries(user_id, entries)
    
    item_entry = ItemEntry(get_item(ITEM_ID_STRAWBERRY), amount)
    item_entry.entry_id = entry_id
    
    inventory.apply_modified_item_entry(item_entry)
    
    vampytest.assert_is(inventory.item_entries, None)
    
    vampytest.assert_is(inventory.item_entries_modified, None)


def test__Inventory__apply_modified_item_entry__no_modifications():
    """
    Tests whether ``Inventory.apply_modified_item_entry`` works as intended.
    
    Case: no modifications.
    """
    user_id = 202503270012
    entries = []
    amount = 10
    entry_id = 5
    
    inventory = Inventory.from_entries(user_id, entries)
    
    item_entry = ItemEntry(get_item(ITEM_ID_STRAWBERRY), amount)
    item_entry.entry_id = entry_id
    
    inventory.apply_modified_item_entry(item_entry)
    
    vampytest.assert_is_not(inventory.item_entries, None)
    vampytest.assert_eq(inventory.item_entries.keys(), {ITEM_ID_STRAWBERRY})
    vampytest.assert_eq(inventory.item_entries[ITEM_ID_STRAWBERRY].amount, amount)
    vampytest.assert_eq(inventory.item_entries[ITEM_ID_STRAWBERRY].entry_id, entry_id)
    
    vampytest.assert_is(inventory.item_entries_modified, None)


def test__Inventory__apply_modified_item_entry__zero():
    """
    Tests whether ``Inventory.apply_modified_item_entry`` works as intended.
    
    Case: setting zero.
    """
    user_id = 202503270013
    entries = []
    amount = 0
    entry_id = 5
    
    inventory = Inventory.from_entries(user_id, entries)
    inventory.modify_item_amount(get_item(ITEM_ID_STRAWBERRY), 0)
    
    item_entry = ItemEntry(get_item(ITEM_ID_STRAWBERRY), amount)
    item_entry.entry_id = entry_id
    
    inventory.apply_modified_item_entry(item_entry)
    
    vampytest.assert_is(inventory.item_entries, None)
    
    vampytest.assert_is(inventory.item_entries_modified, None)


def test__Inventory__apply_modified_item_entry__same_amount():
    """
    Tests whether ``Inventory.apply_modified_item_entry`` works as intended.
    
    Case: same amount.
    """
    user_id = 202503270014
    entries = []
    amount = 5
    entry_id = 5
    
    inventory = Inventory.from_entries(user_id, entries)
    inventory.modify_item_amount(get_item(ITEM_ID_STRAWBERRY), 5)
    
    item_entry = ItemEntry(get_item(ITEM_ID_STRAWBERRY), amount)
    item_entry.entry_id = entry_id
    
    inventory.apply_modified_item_entry(item_entry)
    
    vampytest.assert_is_not(inventory.item_entries, None)
    vampytest.assert_eq(inventory.item_entries.keys(), {ITEM_ID_STRAWBERRY})
    vampytest.assert_eq(inventory.item_entries[ITEM_ID_STRAWBERRY].amount, amount)
    vampytest.assert_eq(inventory.item_entries[ITEM_ID_STRAWBERRY].entry_id, entry_id)
    
    vampytest.assert_is(inventory.item_entries_modified, None)


def test__Inventory__apply_modified_item_entry__different_amount():
    """
    Tests whether ``Inventory.apply_modified_item_entry`` works as intended.
    
    Case: different amount.
    """
    user_id = 202503270015
    entries = []
    amount = 4
    entry_id = 5
    
    inventory = Inventory.from_entries(user_id, entries)
    inventory.modify_item_amount(get_item(ITEM_ID_STRAWBERRY), 5)
    
    item_entry = ItemEntry(get_item(ITEM_ID_STRAWBERRY), amount)
    item_entry.entry_id = entry_id
    
    inventory.apply_modified_item_entry(item_entry)
    
    vampytest.assert_is(inventory.item_entries, None)
    
    vampytest.assert_is_not(inventory.item_entries_modified, None)
    vampytest.assert_eq(inventory.item_entries_modified.keys(), {ITEM_ID_STRAWBERRY})
    vampytest.assert_eq(inventory.item_entries_modified[ITEM_ID_STRAWBERRY].amount, 5)
    vampytest.assert_eq(inventory.item_entries_modified[ITEM_ID_STRAWBERRY].entry_id, entry_id)


def test__Inventory__get_item_entry_by_id__in_entries():
    """
    Tests whether ``Inventory.get_item_entry_by_id`` works as intended.
    
    Case: in entries.
    """
    user_id = 202504010000
    item_id = ITEM_ID_STRAWBERRY
    entries = [
        {
            'id': 6,
            'item_id': ITEM_ID_STRAWBERRY,
            'amount': 2,
        },
    ]
    
    inventory = Inventory.from_entries(user_id, entries)
    
    output = inventory.get_item_entry_by_id(item_id)
    vampytest.assert_instance(output, ItemEntry, nullable = True)
    vampytest.assert_is_not(output, None)
    vampytest.assert_is(output.item.id, item_id)
    

def test__Inventory__get_item_entry_by_id__in_modified_entries():
    """
    Tests whether ``Inventory.get_item_entry_by_id`` works as intended.
    
    Case: in modified entries.
    """
    user_id = 202504010001
    item_id = ITEM_ID_STRAWBERRY
    entries = []
    
    inventory = Inventory.from_entries(user_id, entries)
    inventory.modify_item_amount(get_item(item_id), +2)
    
    output = inventory.get_item_entry_by_id(item_id)
    vampytest.assert_instance(output, ItemEntry, nullable = True)
    vampytest.assert_is_not(output, None)
    vampytest.assert_is(output.item.id, item_id)


def test__Inventory__get_item_entry_by_id__missing():
    """
    Tests whether ``Inventory.get_item_entry_by_id`` works as intended.
    
    Case: missing
    """
    user_id = 202504010002
    item_id = ITEM_ID_STRAWBERRY
    entries = []
    
    inventory = Inventory.from_entries(user_id, entries)
    
    output = inventory.get_item_entry_by_id(item_id)
    vampytest.assert_instance(output, ItemEntry, nullable = True)
    vampytest.assert_is(output, None)


def test__Inventory__get_item_amount__in_entries():
    """
    Tests whether ``Inventory.get_item_amount`` works as intended.
    
    Case: in entries.
    """
    user_id = 202504050002
    item_id = ITEM_ID_STRAWBERRY
    entries = [
        {
            'id': 6,
            'item_id': ITEM_ID_STRAWBERRY,
            'amount': 2,
        },
    ]
    
    inventory = Inventory.from_entries(user_id, entries)
    
    output = inventory.get_item_amount(get_item(item_id))
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)
    

def test__Inventory__get_item_amount__in_modified_entries():
    """
    Tests whether ``Inventory.get_item_amount`` works as intended.
    
    Case: in modified entries.
    """
    user_id = 202504050003
    item_id = ITEM_ID_STRAWBERRY
    entries = []
    
    inventory = Inventory.from_entries(user_id, entries)
    inventory.modify_item_amount(get_item(item_id), +2)
    
    output = inventory.get_item_amount(get_item(item_id))
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 2)


def test__Inventory__get_item_amount__missing():
    """
    Tests whether ``Inventory.get_item_amount`` works as intended.
    
    Case: missing
    """
    user_id = 202504050004
    item_id = ITEM_ID_STRAWBERRY
    entries = []
    
    inventory = Inventory.from_entries(user_id, entries)
    
    output = inventory.get_item_amount(get_item(item_id))
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
