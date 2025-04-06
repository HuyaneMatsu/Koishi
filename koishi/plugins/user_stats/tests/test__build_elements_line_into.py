import vampytest

from ..table_building import build_elements_line_into


def _iter_options():
    yield ([], (), '|')
    yield ([5, 5, 7], ('hey', 'mister', 'sister'), '| hey   | mister | sister  |')


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_elements_line_into(widths, elements):
    """
    Tests whether ``build_elements_line_into`` works as intended.
    
    Parameters
    ----------
    widths : `list<int>`
        Column widths.
    
    elements : `tuple<str>`
        Column elements.
    
    Returns
    -------
    output : `str`
    """
    into = build_elements_line_into([], widths, elements)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into)
