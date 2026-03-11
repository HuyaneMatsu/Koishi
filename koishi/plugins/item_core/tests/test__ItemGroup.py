import vampytest

from ..item_group import ItemGroup


def _assert_fields_set(item_group):
    """
    Asserts whether every fields are set of the given item group.
    
    Parameters
    ----------
    item_group : ``ItemGroup``
        The item group to test.
    """
    vampytest.assert_instance(item_group, ItemGroup)
    vampytest.assert_instance(item_group.id, int)
    vampytest.assert_instance(item_group.name, str)
    vampytest.assert_instance(item_group.item_ids, tuple, nullable = True)


def test__ItemGroup__new():
    """
    Tests whether ``ItemGroup.__new__`` works as intended.
    """
    item_group_id = 99999
    name = 'pudding'
    item_ids = (5, 6)
    
    item_group = ItemGroup(item_group_id, name, item_ids)
    _assert_fields_set(item_group)
    
    vampytest.assert_eq(item_group.id, item_group_id)
    vampytest.assert_eq(item_group.name, name)
    vampytest.assert_eq(item_group.item_ids, item_ids)


def test__ItemGroup__repr():
    """
    Tests whether ``ItemGroup.__repr__`` works as intended.
    """
    item_group_id = 99999
    name = 'pudding'
    item_ids = (5, 6)
    
    item_group = ItemGroup(item_group_id, name, item_ids)
    
    output = repr(item_group)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(item_group).__name__, output)
    vampytest.assert_in(f'id = {item_group_id}', output)
    vampytest.assert_in(f'name = {name!r}', output)
