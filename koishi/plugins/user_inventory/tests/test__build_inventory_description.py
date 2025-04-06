import vampytest

from ...inventory_core import ItemEntry
from ...item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY, get_item

from ..embed_builders import _build_inventory_description


def _iter_options():
    item_peach = get_item(ITEM_ID_PEACH)
    item_strawberry = get_item(ITEM_ID_STRAWBERRY)
    
    yield (
        [
            ItemEntry(item_peach, 4),
            ItemEntry(item_strawberry, 5),
        ],
        (
            f'{item_peach.emoji} {item_peach.name} x4 (0.{4 * item_peach.weight:0>3} kg)\n'
            f'{item_strawberry.emoji} {item_strawberry.name} x5 (0.{5 * item_strawberry.weight:0>3} kg)'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_inventory_description(item_entries):
    """
    Tests whether ``_build_inventory_description`` works as intended.
    
    Parameters
    ----------
    item_entries : `list<ItemEntry>`
        Item entries to render.
    
    Returns
    -------
    output : `str`
    """
    output = _build_inventory_description(item_entries)
    vampytest.assert_instance(output, str)
    return output
