import vampytest

from ..modes import split_by_character


def _iter_options():
    yield (
        'hey mister',
        [
            'h',
            'e',
            'y',
            ' ',
            'm',
            'i',
            's',
            't',
            'e',
            'r',
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__split_by_character(text):
    """
    Tests whether ``split_by_character`` works as intended.
    
    Parameters
    ----------
    text : `str`
        Text to split.
    
    Returns
    -------
    output : `list<str>`
    """
    output = split_by_character(text)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
