import vampytest

from ..embed_builders import produce_inventory_footer


def _iter_options():
    yield 1335, 63122, 'Weight: 1.335 / 63.122 kg'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_inventory_footer(weight, capacity):
    """
    Tests whether ``produce_inventory_footer`` works as intended.
    
    Parameters
    ----------
    weight : `int`
        The weight of the inventory.
    
    capacity : `int`
        Inventory capacity.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_inventory_footer(weight, capacity)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
