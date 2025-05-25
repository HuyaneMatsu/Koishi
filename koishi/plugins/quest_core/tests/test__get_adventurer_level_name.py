import vampytest

from ..utils import get_adventurer_level_name


def _iter_options():
    yield b'A'[0] - b'A'[0], 'H'
    yield b'B'[0] - b'A'[0], 'G'
    yield b'C'[0] - b'A'[0], 'F'
    yield b'D'[0] - b'A'[0], 'E'
    yield b'E'[0] - b'A'[0], 'D'
    yield b'F'[0] - b'A'[0], 'C'
    yield b'G'[0] - b'A'[0], 'B'
    yield b'H'[0] - b'A'[0], 'A'
    yield b'I'[0] - b'A'[0], 'S'
    yield b'J'[0] - b'A'[0], 'S+'
    yield b'K'[0] - b'A'[0], 'S+'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_adventurer_level_name(level):
    """
    Tests whether ``get_adventurer_level_name`` works as intended.
    
    Parameters
    ----------
    level : `int`
        Adventurer level.
    
    Returns
    -------
    output : `str`
    """
    output = get_adventurer_level_name(level)
    vampytest.assert_instance(output, str)
    return output
