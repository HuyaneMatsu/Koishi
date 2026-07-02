import vampytest

from ...item_core import ITEM_ID_CARROT, ITEM_ID_PEACH, get_item_nullable

from ..content_building import produce_butcher_step_description


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
            f'### Butchered {item_peach.emoji} {item_peach.name}\n'
            f'Used energy: 0\n'
            f'Butchered: *none*'
        ),
    )
    
    yield (
        item_peach,
        [
            (item_carrot.id, 20),
            (item_peach.id, 1),
        ],
        66,
        (
            f'### Butchered {item_peach.emoji} {item_peach.name}\n'
            f'Used energy: 66\n'
            f'Butchered:\n'
            f'- 20 {item_carrot.emoji} {item_carrot.name}\n'
            f'- 1 {item_peach.emoji} {item_peach.name}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_butcher_step_description(butchered_item, butcher_amounts, energy_cost):
    """
    Tests whether ``produce_butcher_step_description`` works as intended.
    
    Parameters
    ----------
    butchered_item : ``Item``
        The butchered item.
    
    butcher_amounts : `list(int, int)>`
        Butchered amounts.
    
    energy_cost : `int`
        The used energy.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_butcher_step_description(butchered_item, butcher_amounts, energy_cost)]
    for element in output:
        vampytest.assert_instance(element, str)
    return ''.join(output)
