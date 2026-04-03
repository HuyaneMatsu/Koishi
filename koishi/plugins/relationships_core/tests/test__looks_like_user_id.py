import vampytest

from ..completion_helpers import looks_like_user_id


def _iter_options():
    yield 'm' * 20, False
    yield '1' * 16, False
    yield '1' * 17, True
    yield '1' * 21, True
    yield '1' * 22, False


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__looks_like_user_id(value):
    """
    Tests whether ``looks_like_user_id`` works as intended.
    
    Parameters
    ----------
    value : `str`
        Value to test on.
    
    Returns
    -------
    output : `bool`
    """
    output = looks_like_user_id(value)
    vampytest.assert_instance(output, bool)
    return output
