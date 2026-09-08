import vampytest

from ..loot_packing_and_unpacking import loot_data_iter


def _iter_options():
    yield (
        None,
        [],
    )
    
    yield (
        b''.join([
            (3).to_bytes(1, 'little'), (23).to_bytes(4, 'little'), (10).to_bytes(8, 'little'),
            (1).to_bytes(1, 'little'), (23).to_bytes(4, 'little'), (5).to_bytes(8, 'little'),
        ]),
        [
            (3, 23, 10),
            (1, 23, 5),
        ],
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__loot_data_iter(looted_items):
    """
    Tests whether ``loot_data_iter``.
    
    Parameters
    ----------
    loot_data : `None | bytes`
        Encoded loot data.
    
    Returns
    -------
    output : `list<(int, int, int)>`
    """
    output = [*loot_data_iter(looted_items)]
    
    for element in output:
        vampytest.assert_instance(element, tuple)
        vampytest.assert_eq(len(element), 3)
        vampytest.assert_instance(element[0], int)
        vampytest.assert_instance(element[1], int)
        vampytest.assert_instance(element[2], int)
    
    return output
