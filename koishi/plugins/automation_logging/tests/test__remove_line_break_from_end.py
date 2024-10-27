import vampytest

from ..embed_builder_satori import remove_line_break_from_end


def _iter_options():
    yield (
        ['hey', ' ', 'mister'],
        (
            False,
            ['hey', ' ', 'mister'],
        ),
    )
    yield (
        ['hey', ' ', 'mister', '\n', '\n'],
        (
            False,
            ['hey', ' ', 'mister'],
        ),
    )
    yield (
        ['\n', '\n'],
        (
            True,
            [],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__remove_line_break_from_end(chunk_parts):
    """
    Tests whether ``remove_line_break_from_end`` works as intended.
    
    Parameters
    ----------
    chunk_parts : `list<str>`
        The chunk parts to check.
    
    Returns
    -------
    output : `bool`
    chunk_parts : `list<str>`
    """
    chunk_parts = chunk_parts.copy()
    output = remove_line_break_from_end(chunk_parts)
    vampytest.assert_instance(output, bool)
    return output, chunk_parts
