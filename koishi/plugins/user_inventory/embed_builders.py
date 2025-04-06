__all__ = ()

from hata import Embed

from .constants import SORT_BY_REVERSED_DEFAULT, SORT_BYES_REVERSED, SORT_ORDER_REVERSED_DEFAULT, SORT_ORDERS_REVERSED


def _render_weight_into(weight, into):
    """
    Renders the given weight.
    
    Parameters
    ----------
    weight : `int`
        Weight in grams.
    
    into : `list<str>`
        Container to extend.
    
    Returns
    -------
    into : `list<str>`
    """
    kilo_grams, grams = divmod(weight, 1000)
    into.append(str(kilo_grams))
    into.append('.')
    grams_string = str(grams)
    into.append('0' * (3 - len(grams_string)))
    into.append(grams_string)
    return into


def _build_inventory_description(item_entries):
    """
    Builds inventory description.
    
    Parameters
    ----------
    item_entries : `list<ItemEntry>`
        Item entries to render.
    
    Returns
    -------
    description : `str`
    """
    description_parts = []
    item_added = False
    
    for item_entry in item_entries:
        if item_added:
            description_parts.append('\n')
        else:
            item_added = True
        
        item = item_entry.item
        emoji = item.emoji
        if (emoji is not None):
            description_parts.append(emoji.as_emoji)
            description_parts.append(' ')
        
        description_parts.append(item.name)
        description_parts.append(' x')
        
        amount = item_entry.amount
        
        description_parts.append(str(amount))
        
        description_parts.append(' (')
        description_parts = _render_weight_into(amount * item.weight, description_parts)
        description_parts.append(' kg)')
    
    return ''.join(description_parts)


def _build_inventory_footer(weight, capacity):
    """
    Builds inventory footer.
    
    Parameters
    ----------
    weight : `int`
        The weight of the inventory.
    
    capacity : `int`
        Inventory capacity.
    
    Returns
    -------
    description : `str`
    """
    footer_parts = []
    
    # Weight
    footer_parts.append('Weight: ')
    footer_parts = _render_weight_into(weight, footer_parts)
    footer_parts.append(' / ')
    footer_parts = _render_weight_into(capacity, footer_parts)
    footer_parts.append(' kg')
    
    return ''.join(footer_parts)


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
        _build_inventory_description(item_entries),
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
        _build_inventory_footer(weight, capacity),
    )
