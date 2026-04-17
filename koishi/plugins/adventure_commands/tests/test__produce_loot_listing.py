import vampytest

from ...adventure_core import (
    LOOT_STATE_SUCCESS, LOOT_STATE_LOST_DUE_FULL_INVENTORY, LOOT_STATE_LOST_DUE_LOW_ENERGY,
)
from ...item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY, get_item_nullable

from ..component_building import produce_loot_listing


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    item_strawberry = get_item_nullable(ITEM_ID_STRAWBERRY)
    assert item_peach is not None
    assert item_strawberry is not None
    
    yield (
        {},
        '',
    )
    
    yield (
        {
            LOOT_STATE_SUCCESS : {
                ITEM_ID_PEACH : 11,
            },
        },
        (
            f'### Loot:\n'
            f'- {item_peach.emoji} {item_peach.name} x11 ({item_peach.weight * 11 / 1000:.03f} kg)'
        ),
    )
    
    yield (
        {
            LOOT_STATE_SUCCESS : {
                ITEM_ID_PEACH : 11,
            },
            LOOT_STATE_LOST_DUE_FULL_INVENTORY : {
                ITEM_ID_PEACH : 4,
                ITEM_ID_STRAWBERRY : 7,
            },
            LOOT_STATE_LOST_DUE_LOW_ENERGY : {
                ITEM_ID_PEACH : 3,
            },
        },
        (
            f'### Loot:\n'
            f'- {item_peach.emoji} {item_peach.name} x11 ({item_peach.weight * 11 / 1000:.03f} kg)\n'
            f'### Loot lost due to low energy:\n'
            f'- {item_peach.emoji} {item_peach.name} x3 ({item_peach.weight * 3 / 1000:.03f} kg)\n'
            f'### Loot lost due to full inventory:\n'
            f'- {item_peach.emoji} {item_peach.name} x4 ({item_peach.weight * 4 / 1000:.03f} kg)\n'
            f'- {item_strawberry.emoji} {item_strawberry.name} x7 ({item_strawberry.weight * 7 / 1000:.03f} kg)'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_loot_listing(grouped_loot):
    """
    Tests whether ``produce_loot_listing`` works as intended.
    
    Parameters
    ----------
    grouped_loot : `dict<int, dict<int, int>>`
        Grouped loot by state.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_loot_listing(grouped_loot)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
