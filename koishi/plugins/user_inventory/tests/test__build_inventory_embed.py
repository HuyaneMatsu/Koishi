import vampytest
from hata import Embed

from ...inventory_core import ItemEntry
from ...item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY, get_item

from ..embed_builders import build_inventory_embed


def _iter_options():
    item_peach = get_item(ITEM_ID_PEACH)
    item_strawberry = get_item(ITEM_ID_STRAWBERRY)
    
    yield (
        [
            ItemEntry(item_peach, 4),
            ItemEntry(item_strawberry, 5),
        ],
        1,
        0,
        0,
        1335,
        63122,
        Embed(
            'Inventory',
            (
                f'{item_peach.emoji} {item_peach.name} x4 (0.{4 * item_peach.weight:0>3} kg)\n'
                f'{item_strawberry.emoji} {item_strawberry.name} x5 (0.{5 * item_strawberry.weight:0>3} kg)'
            ),
        ).add_field(
            'Page',
            (
                f'```\n'
                f'2\n'
                f'```'
            ),
            True,
        ).add_field(
            'Sort by',
            (
                f'```\n'
                f'name\n'
                f'```'
            ),
            True,
        ).add_field(
            'Sort order',
            (
                f'```\n'
                f'increasing\n'
                f'```'
            ),
            True,
        ).add_footer(
            'Weight: 1.335 / 63.122 kg'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_inventory_embed(item_entries, page_index, sort_by, sort_order, weight, capacity):
    """
    Tests whether ``build_inventory_embed`` works as intended.
    
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
    output : ``Embed``
    """
    output = build_inventory_embed(item_entries, page_index, sort_by, sort_order, weight, capacity)
    vampytest.assert_instance(output, Embed)
    return output
