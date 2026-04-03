import vampytest

from ..content_building import produce_int_block


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
def test_produce_int_block(value):
    """
    Tests whether ``produce_int_block`` works as intended.
    
    Parameters
    ----------
    value : `int`
        The value to produce.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_int_block(value)]
    for element in output:
        vampytest.assert_instance(element, str)
    return ''.join(output)
