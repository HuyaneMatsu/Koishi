import vampytest

from ..helpers import produce_length_bytes


def _iter_options():
    yield 0, (0).to_bytes(1, 'little')
    yield 1, (1).to_bytes(1, 'little')
    yield 63, (63).to_bytes(1, 'little')
    yield 64, (64 | 1).to_bytes(1, 'little') + (64).to_bytes(1, 'little') 
    yield 255, (64 | 1).to_bytes(1, 'little') + (255).to_bytes(1, 'little') 
    yield 256, (64 | 2).to_bytes(1, 'little') + (256).to_bytes(2, 'little')


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_length_bytes(length):
    """
    Tests whether ``produce_length_bytes`` works as intended.
    
    Parameters
    ----------
    length : `int`
        The length to convert.
    
    Returns
    -------
    output : `bytes`
    """
    parts = [*produce_length_bytes(length)]
    for element in parts:
        vampytest.assert_instance(element, bytes)
    
    return b''.join(parts)
