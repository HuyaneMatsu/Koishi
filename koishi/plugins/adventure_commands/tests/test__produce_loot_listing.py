import vampytest
from hata import BUILTIN_EMOJIS

from ...adventure_core import (
    LOOT_STATE_SUCCESS, LOOT_STATE_LOST_DUE_FULL_INVENTORY, LOOT_STATE_LOST_DUE_LOW_ENERGY,
)
from ...item_core import ITEM_ID_PEACH, ITEM_ID_STRAWBERRY

from ..component_builders import produce_loot_listing


def _iter_options():
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
            f'- {BUILTIN_EMOJIS["peach"]} Peach x11'
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
            f'- {BUILTIN_EMOJIS["peach"]} Peach x11\n'
            f'### Loot lost due to low energy:\n'
            f'- {BUILTIN_EMOJIS["peach"]} Peach x3\n'
            f'### Loot lost due to full inventory:\n'
            f'- {BUILTIN_EMOJIS["peach"]} Peach x4\n'
            f'- {BUILTIN_EMOJIS["strawberry"]} Strawberry x7'
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
