__all__ = (
    'get_item', 'get_item_group', 'get_item_group_name', 'get_item_group_nullable', 'get_item_name',
    'get_item_nullable', 'produce_item_flags_names', 'produce_item_flags_with_names',
    'produce_item_group_id_with_name', 'produce_item_id_with_name'
)

from .constants import (
    ITEM_DESCRIPTION_DEFAULT, ITEM_EMOJI_DEFAULT, ITEM_FLAG_NAME_DEFAULT, ITEM_GROUP_NAME_DEFAULT, ITEM_GROUPS,
    ITEM_NAME_DEFAULT, ITEMS
)
from .flags import ITEM_FLAG_NAMES

from .item import Item
from .item_group import ItemGroup


def get_item_nullable(item_id):
    """
    Gets the item allowing returning `None`.
    
    Parameters
    ----------
    item_id : `int`
        The item identifier.
    
    Returns
    -------
    item : ``None | Item``
    """
    if item_id:
        try:
            return ITEMS[item_id]
        except KeyError:
            pass


def get_item_group_nullable(item_group_id):
    """
    Gets the item group allowing returning `None`.
    
    Parameters
    ----------
    item_group_id : `int`
        The item group's identifier.
    
    Returns
    -------
    item_group : ``None | ItemGroup``
    """
    if item_group_id:
        try:
            return ITEM_GROUPS[item_group_id]
        except KeyError:
            pass


def get_item(item_id):
    """
    Gets the item for the given identifier.
    
    Parameters
    ----------
    item_id : `int`
        The item identifier.
    
    Returns
    -------
    item : ``Item``
    """
    try:
        return ITEMS[item_id]
    except KeyError:
        pass
    
    item = Item(
        item_id,
        ITEM_NAME_DEFAULT,
        ITEM_EMOJI_DEFAULT,
        ITEM_DESCRIPTION_DEFAULT,
        0,
        0,
        0,
        None,
    )
    
    ITEMS[item_id] = item
    return item


def get_item_group(item_group_id):
    """
    Gets the item group for the given identifier.
    
    Parameters
    ----------
    item_group_id : `int`
        The item group's identifier.
    
    Returns
    -------
    item_group : ``ItemGroup``
    """
    try:
        return ITEM_GROUPS[item_group_id]
    except KeyError:
        pass
    
    item_group = ItemGroup(
        item_group_id,
        ITEM_GROUP_NAME_DEFAULT,
        None,
    )
    
    ITEM_GROUPS[item_group_id] = item_group
    return item_group


def get_item_name(item_id):
    """
    Gets the item's name.
    
    Parameters
    ----------
    item_id : `int`
        The item identifier.
    
    Returns
    -------
    item_name : `str`
    """
    try:
        item = ITEMS[item_id]
    except KeyError:
        item_name = ITEM_NAME_DEFAULT
    else:
        item_name = item.name
    
    return item_name


def get_item_group_name(item_group_id):
    """
    Gets the item's name.
    
    Parameters
    ----------
    item_group_id : `int`
        The item group's identifier.
    
    Returns
    -------
    item_group_name : `str`
    """
    try:
        group = ITEM_GROUPS[item_group_id]
    except KeyError:
        item_group_name = ITEM_GROUP_NAME_DEFAULT
    else:
        item_group_name = group.name
    
    return item_group_name


def produce_item_flags_names(item_flags, separator):
    """
    Produces representation for each specific bit flag.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item_flags : `int`
        Item's flags.
    
    separator : `str`
        Separator to use.
    
    Yields
    ------
    part : `str`
    """
    flag_yielded = False
    
    for index, name in enumerate(ITEM_FLAG_NAMES):
        if not (item_flags & (1 << index)):
            continue
        
        if flag_yielded:
            yield separator
        else:
            flag_yielded = True
        
        yield name
        continue
    
    if not flag_yielded:
        yield ITEM_FLAG_NAME_DEFAULT


def produce_item_id_with_name(item_id):
    """
    Produces item identifier with its name.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item_id : `int`
        Item identifier.
    
    Yields
    ------
    part : `str`
    """
    yield repr(item_id)
    yield ' ('
    yield get_item_name(item_id)
    yield ')'


def produce_item_group_id_with_name(item_group_id):
    """
    Produces item identifier with its name.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item_group_id : `int`
        Item group identifier.
    
    Yields
    ------
    part : `str`
    """
    yield repr(item_group_id)
    yield ' ('
    yield get_item_group_name(item_group_id)
    yield ')'


def produce_item_flags_with_names(item_flags):
    """
    Produces item identifier with its name.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item_flags : `int`
        Item's flags.
    
    Yields
    ------
    part : `str`
    """
    yield repr(item_flags)
    yield ' ('
    yield from produce_item_flags_names(item_flags, ' | ')
    yield ')'
