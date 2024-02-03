import vampytest

from ..value_renderers import render_index_into


def test__render_index_into():
    """
    Tests whether ``render_index_into`` works as intended.
    """
    index = 6
    
    into = render_index_into([], index)
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    output = ''.join(into)
    
    vampytest.assert_eq(output, f'{index!s}.: ')
