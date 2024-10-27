import vampytest

from ..embed_builder_satori import add_chunk


def _iter_options():
    yield (
        ['hey', ' ', 'mister'],
        ['hey mister'],
    )
    yield (
        ['hey', ' ', 'mister', '\n', '\n'],
        ['hey mister'],
    )
    yield (
        ['\n', '\n'],
        [],
    )



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__add_chunk(chunk_parts):
    """
    Tests whether ``add_chunk`` works as intended.
    
    Parameters
    ----------
    chunk_parts : `list<str>`
        The chunk parts to check.
    
    Returns
    -------
    chunks : `list<str>`
    """
    chunks = []
    chunk_parts = chunk_parts.copy()
    add_chunk(chunks, chunk_parts)
    vampytest.assert_false(chunk_parts)
    return chunks
