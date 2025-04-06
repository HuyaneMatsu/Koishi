import vampytest

from ..table_building import build_separator_line


def _iter_options():
    yield ([3, 5, 7], '-', '+-----+-------+---------+')
    yield ([3, 5, 7], '=', '+=====+=======+=========+')
    yield ([3, 5, 0], '-', '+-----+-------+--+')


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_separator_line(widths, character):
    """
    Tests whether ``build_separator_line`` works as intended.
    
    Parameters
    ----------
    widths : `list<int>`
        Column widths.
    
    character : `str`
        Separator character.
    
    Returns
    -------
    output : `str`
    """
    output = build_separator_line(widths, character)
    vampytest.assert_instance(output, str)
    return output
