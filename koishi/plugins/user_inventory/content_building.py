__all__ = ()

from ..item_core import produce_weight

from .constants import SORT_BY_REVERSED_DEFAULT, SORT_BYES_REVERSED, SORT_ORDER_REVERSED_DEFAULT, SORT_ORDERS_REVERSED


def produce_inventory_header(user, guild_id, page_index, sort_by, sort_order, weight, capacity):
    """
    Builds inventory embed.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's inventory is being rendered.
    
    guild_id : `int`
        The local guild's identifier.
    
    page_index : `int`
        The current page's index.
    
    sort_by : `int`
        Identifier to determine how item entries should be sorted.
    
    sort_order : `int`
        Identifier to determine sorting order.
    
    weight : `int`
        The weight of the inventory.
    
    capacity : `int`
        Inventory capacity.
    
    Yields
    ------
    part : `str`
    """
    yield '# '
    yield user.name_at(guild_id)
    yield '\'s inventory\n\nPage: '
    yield str(page_index + 1)
    yield '; Sort by: '
    yield SORT_BYES_REVERSED.get(sort_by, SORT_BY_REVERSED_DEFAULT)
    yield '; Sort order: '
    yield SORT_ORDERS_REVERSED.get(sort_order, SORT_ORDER_REVERSED_DEFAULT)
    yield '\nWeight: '
    yield from produce_weight(weight)
    yield ' / '
    yield from produce_weight(capacity)
    yield ' kg'


def produce_inventory_description(item_entries):
    """
    Produces inventory description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item_entries : `list<ItemEntry>`
        Item entries to render.
    
    Yields
    ------
    part : `str`
    """
    item_added = False
    
    for item_entry in item_entries:
        if item_added:
            yield '\n'
        else:
            item_added = True
        
        item = item_entry.item
        emoji = item.emoji
        if (emoji is not None):
            yield emoji.as_emoji
            yield ' '
        
        yield item.name
        yield ' x'
        
        amount = item_entry.amount
        
        yield str(amount)
        
        yield ' ('
        yield from produce_weight(amount * item.weight)
        yield ' kg)'
