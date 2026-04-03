import vampytest

from ..rendering import _produce_creator


def _iter_options():
    yield (
        'sister',
        (
            '.with_creator(\n'
            '    \'sister\',\n'
            ')'
        ),
    )
    
    yield (
        None,
        (
            ''
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_creator(creator):
    """
    Tests whether ``_produce_creator`` works as intended.
    
    Parameters
    ----------
    creator : `None | str`
        Image creator.
    
    Returns
    -------
    output : `str`
    """
    output = [*_produce_creator(creator)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
