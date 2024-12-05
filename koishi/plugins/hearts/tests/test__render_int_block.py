import vampytest

from ..rendering import render_int_block


def _iter_options():
    yield (
        5,
        (
            '```\n'
            '5\n'
            '```'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test_render_int_block(value):
    """
    Tests whether ``render_int_block`` works as intended.
    
    Parameters
    ----------
    value : `int`
        The value to render.
    
    Returns
    -------
    output : `str`
    """
    output = render_int_block(value)
    vampytest.assert_instance(output, str)
    return output
