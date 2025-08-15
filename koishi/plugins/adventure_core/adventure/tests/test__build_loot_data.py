import vampytest

from ..loot_packing_and_unpacking import build_loot_data


def _iter_options():
    yield (
        None,
        None,
    )
    
    yield (
        [
            (3, 23, 10),
            (1, 23, 5),
        ],
        b''.join([
            (3).to_bytes(1, 'little'), (23).to_bytes(4, 'little'), (10).to_bytes(8, 'little'),
            (1).to_bytes(1, 'little'), (23).to_bytes(4, 'little'), (5).to_bytes(8, 'little'),
        ]),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_loot_data(looted_items):
    """
    Tests whether ``build_loot_data``.
    
    Parameters
    ----------
    looted_items : `list<(int, int, int)>`
        A list of tuple of 3 elements: loot state, item id and given amount.
    
    Returns
    -------
    output : `None | bytes`
    """
    output = build_loot_data(looted_items)
    vampytest.assert_instance(output, bytes, nullable = True)
    return output
