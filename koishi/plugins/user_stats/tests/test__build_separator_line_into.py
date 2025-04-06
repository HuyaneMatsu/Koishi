import vampytest

from ..table_building import build_separator_line_into


def _iter_options():
    yield ([3, 5, 7], '-', '+-----+-------+---------+')
    yield ([3, 5, 7], '=', '+=====+=======+=========+')
    yield ([3, 5, 0], '-', '+-----+-------+--+')


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_separator_line_into(widths, character):
    """
    Tests whether ``build_separator_line_into`` works as intended.
    
    parameters
    ----------
    widths : `list<int>`
        Column widths.
    
    character : `str`
        Separator character.
    
    Returns
    -------
    output : `str`
    """
    into = build_separator_line_into([], widths, character)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into)
