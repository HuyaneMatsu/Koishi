__all__ = ()

from hata import Embed

from ..item_core import produce_weight

from .constants import SORT_BY_REVERSED_DEFAULT, SORT_BYES_REVERSED, SORT_ORDER_REVERSED_DEFAULT, SORT_ORDERS_REVERSED


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


def produce_inventory_footer(weight, capacity):
    """
    Produces inventory footer.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    weight : `int`
        The weight of the inventory.
    
    capacity : `int`
        Inventory capacity.
    
    Yields
    -------
    part : `str`
    """
    footer_parts = []
    
    # Weight
    yield 'Weight: '
    yield from produce_weight(weight)
    yield ' / '
    yield from produce_weight(capacity)
    yield ' kg'


def build_inventory_embed(item_entries, page_index, sort_by, sort_order, weight, capacity):
    """
    Builds inventory embed.
    
    Parameters
    ----------
    item_entries : `list<ItemEntry>`
        Item entries to render.
    
    page_index : `int`
        The current page's index.
    
    sort_by : `int`
        Identifier to determine how item entries should be sorted.
    
    sort_order : `int`
        Identifier to determine sorting order.
    
    page_count : `int`
        Amount of pages.
    
    weight : `int`
        The weight of the inventory.
    
    capacity : `int`
        Inventory capacity.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Inventory',
        ''.join([*produce_inventory_description(item_entries)]),
    ).add_field(
        'Page',
        (
            f'```\n'
            f'{page_index + 1}\n'
            f'```'
        ),
        True,
    ).add_field(
        'Sort by',
        (
            f'```\n'
            f'{SORT_BYES_REVERSED.get(sort_by, SORT_BY_REVERSED_DEFAULT)}\n'
            f'```'
        ),
        True,
    ).add_field(
        'Sort order',
        (
            f'```\n'
            f'{SORT_ORDERS_REVERSED.get(sort_order, SORT_ORDER_REVERSED_DEFAULT)}\n'
            f'```'
        ),
        True,
    ).add_footer(
        ''.join([*produce_inventory_footer(weight, capacity)]),
    )
