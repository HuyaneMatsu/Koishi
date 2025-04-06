import vampytest
from hata import BUILTIN_EMOJIS, Emoji

from ...item_modifier_core import Modifier, MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT, MODIFIER_KIND__PERCENT, construct_modifier_type

from ..flags import ITEM_FLAG_EDIBLE
from ..item import Item


def _assert_fields_set(item):
    """
    Asserts whether every fields are set of the given item.
    
    Parameters
    ----------
    item : ``Item``
        The item to test.
    """
    vampytest.assert_instance(item, Item)
    vampytest.assert_instance(item.description, str)
    vampytest.assert_instance(item.emoji, Emoji, nullable = True)
    vampytest.assert_instance(item.flags, int)
    vampytest.assert_instance(item.id, int)
    vampytest.assert_instance(item.name, str)
    vampytest.assert_instance(item.modifiers, tuple, nullable = True)
    vampytest.assert_instance(item.weight, int)


def test__Item__new():
    """
    Tests whether ``Item.__new__`` works as intended.
    """
    description = 'pudding <3'
    emoji = BUILTIN_EMOJIS['custard']
    flags = ITEM_FLAG_EDIBLE
    item_id = 99999
    modifiers = (Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT), 20),)
    name = 'pudding'
    value = 6
    weight = 32
    
    item = Item(item_id, name, emoji, description, flags, value, weight, modifiers)
    _assert_fields_set(item)
    
    vampytest.assert_eq(item.description, description)
    vampytest.assert_is(item.emoji, emoji)
    vampytest.assert_eq(item.flags, flags)
    vampytest.assert_eq(item.id, item_id)
    vampytest.assert_eq(item.name, name)
    vampytest.assert_eq(item.modifiers, modifiers)
    vampytest.assert_eq(item.value, value)
    vampytest.assert_eq(item.weight, weight)


def test__Item__repr():
    """
    Tests whether ``Item.__repr__`` works as intended.
    """
    description = 'pudding <3'
    emoji = BUILTIN_EMOJIS['custard']
    flags = ITEM_FLAG_EDIBLE
    item_id = 99999
    modifiers = (Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT), 20),)
    name = 'pudding'
    value = 6
    weight = 32
    
    item = Item(item_id, name, emoji, description, flags, value, weight, modifiers)
    
    output = repr(item)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(item).__name__, output)
    vampytest.assert_in(f'name = {name!r}', output)
    vampytest.assert_in(f'id = {item_id}', output)


def test__Item__iter_modifiers__0():
    """
    Tests whether ``Item.iter_modifiers`` works as intended.
    
    Case: 0.
    """
    description = 'pudding <3'
    emoji = BUILTIN_EMOJIS['custard']
    flags = ITEM_FLAG_EDIBLE
    item_id = 99999
    modifiers = None
    name = 'pudding'
    value = 6
    weight = 32
    
    item = Item(item_id, name, emoji, description, flags, value, weight, modifiers)
     
    vampytest.assert_eq(
        [*item.iter_modifiers()],
        [],
    )


def test__Item__iter_modifiers__2():
    """
    Tests whether ``Item.iter_modifiers`` works as intended.
    
    Case: 2.
    """
    modifier_0 = Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT), 20)
    modifier_1 = Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__PERCENT), 20)
    
    description = 'pudding <3'
    emoji = BUILTIN_EMOJIS['custard']
    flags = ITEM_FLAG_EDIBLE
    item_id = 99999
    modifiers = (modifier_0, modifier_1)
    name = 'pudding'
    value = 6
    weight = 32
    
    item = Item(item_id, name, emoji, description, flags, value, weight, modifiers)
     
    vampytest.assert_eq(
        [*item.iter_modifiers()],
        [modifier_0, modifier_1],
    )
