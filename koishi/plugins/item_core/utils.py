__all__ = ('get_item', 'get_item_name', 'get_item_nullable')

from .constants import ITEM_DESCRIPTION_DEFAULT, ITEM_EMOJI_DEFAULT, ITEM_NAME_DEFAULT, ITEMS

from .item import Item


def get_item_nullable(item_id):
    """
    Gets the item allowing returning `None`.
    
    Parameters
    ----------
    item_id : `int`
        The item identifier.
    
    Returns
    -------
    item : ``Item``
    """
    if item_id:
        try:
            return ITEMS[item_id]
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
