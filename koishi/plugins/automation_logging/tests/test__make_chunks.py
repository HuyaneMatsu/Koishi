import vampytest

from ..embed_builder_satori import make_chunks


def _iter_options():
    yield ['hey', ' ', 'mister'], ['hey mister']
    yield ['hey', ' ', 'mister', '\n', '\n'], ['hey mister']
    yield ['hey', ' ', 'mister', '\n', 'sister'], ['hey mister', 'sister']
    yield ['hey', '\n', 'hello', '\n', 'hell'], ['hey\nhello', 'hell']


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__make_chunks(parts):
    """
    Tests whether ``make_chunks`` works as intended.
    
    Parameters
    ----------
    parts : `list<str>`
        Content parts to chunk.
    
    Returns
    -------
    output : `list<str>`
    """
    output = vampytest.mock_globals(make_chunks, MAX_CHUNK_SIZE = 20, BREAK_AFTER_LENGTH = 8)(parts)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, str)
    return output
