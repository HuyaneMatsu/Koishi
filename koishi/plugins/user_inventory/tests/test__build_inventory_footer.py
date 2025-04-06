import vampytest

from ..embed_builders import _build_inventory_footer


def _iter_options():
    yield 1335, 63122, 'Weight: 1.335 / 63.122 kg'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_inventory_footer(weight, capacity):
    """
    Tests whether ``_build_inventory_footer`` works as intended.
    
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
    output = _build_inventory_footer(weight, capacity)
    vampytest.assert_instance(output, str)
    return output
