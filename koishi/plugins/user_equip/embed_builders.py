__all__ = (
    'build_failure_embed_empty_equipment_slot', 'build_failure_embed_no_equipment_like',
    'build_failure_embed_same_item', 'build_success_embed_item_equipped', 'build_success_embed_item_unequipped',
    'build_success_embed_item_replaced'
)

from hata import Embed

from .constants import ITEM_SLOT_NAME_UNKNOWN, ITEM_SLOT_NAMES


def build_failure_embed_no_equipment_like(item_flag, value):
    """
    Builds a failure embed for the case when there is no equipment like the given item name.
    
    Parameters
    ----------
    item_flag : `int`
        The item flag to filter for.
    
    value : `str`
        The item's name to select.
    
    Returns
    -------
    embed : ``Embed``
    """
    item_slot_name = ITEM_SLOT_NAMES.get(item_flag, ITEM_SLOT_NAME_UNKNOWN)
    
    return Embed(
        'Oh no',
        f'Cannot equip {value!s} as {item_slot_name!s}.',
    )


def build_failure_embed_same_item(item_flag, item):
    """
    Builds a failure embed for the case when the item to equip is the same as the equipped item.
    
    Parameters
    ----------
    item_flag : `int`
        The item flag to filter for.
    
    item : ``Item``
        The selected item.
    
    Returns
    -------
    embed : ``Embed``
    """
    item_slot_name = ITEM_SLOT_NAMES.get(item_flag, ITEM_SLOT_NAME_UNKNOWN)
    
    return Embed(
        'Oh no',
        f'Are you sure you do not have {item.name} already equipped as {item_slot_name!s}?',
    )


def build_success_embed_item_equipped(item_flag, item):
    """
    Builds a success embed when the selected item was equipped and there was no previously equipped item.
    
    Parameters
    ----------
    item_flag : `int`
        The item flag to filter for.
    
    item : ``Item``
        The selected item.
    
    Returns
    -------
    embed : ``Embed``
    """
    item_slot_name = ITEM_SLOT_NAMES.get(item_flag, ITEM_SLOT_NAME_UNKNOWN)
    
    return Embed(
        'Great success!',
        f'You equipped {item.name} as your {item_slot_name!s}.',
    )


def build_success_embed_item_replaced(item_flag, old_item, new_item):
    """
    Builds a success embed when the selected item was equipped replacing an other one.
    
    Parameters
    ----------
    item_flag : `int`
        The item flag to filter for.
    
    old_item : ``Item``
        The removed item.
    
    new_item : ``Item``
        The selected item.
    
    Returns
    -------
    embed : ``Embed``
    """
    item_slot_name = ITEM_SLOT_NAMES.get(item_flag, ITEM_SLOT_NAME_UNKNOWN)
    
    return Embed(
        'Great success!',
        f'You equipped {new_item.name} as your {item_slot_name!s}, unequipping {old_item.name}.',
    )


def build_failure_embed_empty_equipment_slot(item_flag):
    """
    Builds a failure embed when there is no item in the equipment solt, therefore it cannot be removed.
    
    Parameters
    ----------
    item_flag : `int`
        The item type to remove.
    
    Returns
    -------
    embed : ``Embed``
    """
    item_slot_name = ITEM_SLOT_NAMES.get(item_flag, ITEM_SLOT_NAME_UNKNOWN)
    
    return Embed(
        'Oh no',
        f'You do not have any item equipped as {item_slot_name!s}.',
    )


def build_success_embed_item_unequipped(item_flag, item):
    """
    Builds a success embed when the item from the selected slot was unequipped.
    
    Parameters
    ----------
    item_flag : `int`
        The item type slot to unequip.
    
    item : ``Item``
        The unequipped item.
    
    Returns
    -------
    embed : ``Embed``
    """
    item_slot_name = ITEM_SLOT_NAMES.get(item_flag, ITEM_SLOT_NAME_UNKNOWN)
    
    return Embed(
        'Great success!',
        f'You unequipped your {item_slot_name!s}, {item.name}.',
    )
