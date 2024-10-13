import vampytest

from ..building import _within_title


def _iter_options():
    yield 'koishi', 'koishi: hey\n'
    yield 'mister', 'mister: hey\n'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__within_title(title):
    """
    Tests whether ``_within_title`` works as intended.
    
    Parameters
    ----------
    title : `str`
        Title to start with.
    
    Returns
    -------
    output : `str`
    """
    output = []
    for _ in _within_title(title, output):
        output.append('hey')
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
