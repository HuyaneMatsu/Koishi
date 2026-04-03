import vampytest

from ..modes import split_no_split


def _iter_options():
    yield (
        'hey mister',
        [
            'hey mister',
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__split_no_split(text):
    """
    Tests whether ``split_no_split`` works as intended.
    
    Parameters
    ----------
    text : `str`
        Text to split.
    
    Returns
    -------
    output : `list<str>`
    """
    output = split_no_split(text)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
