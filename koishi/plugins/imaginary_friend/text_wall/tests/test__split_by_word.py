import vampytest

from ..modes import split_by_word


def _iter_options():
    yield (
        'hey mister',
        [
            'hey',
            'mister',
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__split_by_word(text):
    """
    Tests whether ``split_by_word`` works as intended.
    
    Parameters
    ----------
    text : `str`
        Text to split.
    
    Returns
    -------
    output : `list<str>`
    """
    output = split_by_word(text)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
