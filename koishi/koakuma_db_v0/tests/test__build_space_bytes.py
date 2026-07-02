import vampytest

from ..helpers import build_space_bytes


def _iter_options():
    yield 0, (128).to_bytes(1, 'little')
    yield 1, (128 | 1).to_bytes(1, 'little')
    yield 63, (128 | 63).to_bytes(1, 'little')
    yield 64, (128 | 64 | 1).to_bytes(1, 'little') + (64).to_bytes(1, 'little') 
    yield 255, (128 | 64 | 1).to_bytes(1, 'little') + (255).to_bytes(1, 'little') 
    yield 256, (128 | 64 | 2).to_bytes(1, 'little') + (256).to_bytes(2, 'little')


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_space_bytes(length):
    """
    Tests whether ``build_space_bytes`` works as intended.
    
    Parameters
    ----------
    length : `int`
        The length to convert.
    
    Returns
    -------
    output : `bytes`
    """
    output = build_space_bytes(length)
    vampytest.assert_instance(output, bytes)
    return output
