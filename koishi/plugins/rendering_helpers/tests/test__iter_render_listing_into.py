import vampytest

from ..value_renderers import iter_render_listing_into


def test__iter_render_listing_into__truncated():
    """
    Tests whether ``iter_render_listing_into`` works as intended.
    
    Case: Output truncated.
    """
    into = []
    
    for element in iter_render_listing_into(into, [*range(10, 20)], 2):
        into.append(str(element))
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    output = ''.join(into)
    
    vampytest.assert_eq(
        output,
        (
            '1.: 10\n'
            '2.: 11\n'
            '(8 truncated)'
        ),
    )


def test__iter_render_listing_into__non_truncated():
    """
    Tests whether ``iter_render_listing_into`` works as intended.
    
    Case: Output not truncated.
    """
    into = []
    
    for element in iter_render_listing_into(into, [*range(10, 12)], 4):
        into.append(str(element))
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    output = ''.join(into)
    
    vampytest.assert_eq(
        output,
        (
            '1.: 10\n'
            '2.: 11'
        ),
    )
