import vampytest

from ...item_core import ITEM_ID_CARROT, ITEM_ID_PEACH, get_item_nullable

from ..content_building import produce_butcher_item_description


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    item_carrot = get_item_nullable(ITEM_ID_CARROT)
    assert item_carrot is not None
    
    yield (
        item_peach,
        None,
        0,
        (
            f'### Butcher {item_peach.emoji} {item_peach.name} costing up to 0 energy, for: *none*'
        ),
    )
    
    yield (
        item_peach,
        [
            (item_carrot.id, 0.5, 20),
            (item_peach.id, 0.1, 1),
        ],
        66,
        (
            f'### Butcher {item_peach.emoji} {item_peach.name} costing up to 66 energy, for:\n'
            f'- 50% chance of 20 {item_carrot.emoji} {item_carrot.name}\n'
            f'- 10% chance of 1 {item_peach.emoji} {item_peach.name}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_butcher_item_description(item, loot_chance_and_amounts, energy_cost):
    """
    Tests whether ``produce_butcher_item_description`` works as intended.
    
    Parameters
    ----------
    item : ``Item``
        Item to butcher.
    
    loot_chance_and_amounts : `None | list<(int, float, int)>`
        Loot chances and amounts.
    
    energy_cost : `int`
        Upper energy cost.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_butcher_item_description(item, loot_chance_and_amounts, energy_cost)]
    for element in output:
        vampytest.assert_instance(element, str)
    return ''.join(output)
