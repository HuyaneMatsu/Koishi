import vampytest

from ..rendering import _produce_to_do


def _iter_options():
    yield (
        None,
        (
            '# TODO\n'
        ),
    )
    
    yield (
        {'hey', 'mister'},
        (
            '# TODO hey mister\n'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_to_do(unidentified):
    """
    Tests whether ``_produce_to_do`` works as intended.
    
    Parameters
    ----------
    unidentified : `None | set<str>`
        Unidentified name parts.
    
    Returns
    -------
    output : `str`
    """
    output = [*_produce_to_do(unidentified)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
