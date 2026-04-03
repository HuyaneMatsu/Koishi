import vampytest

from ..related_completion import remove_comment


def _iter_options():
    yield 'koishi', 'koishi'
    yield 'koishi (6 days)', 'koishi'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__remove_comment(target_user_name):
    """
    Tests whether ``remove_comment`` works as intended.
    
    Parameters
    ----------
    target_user_name : `str`
        The target user's name.
    
    Returns
    -------
    output : `str`
    """
    output = remove_comment(target_user_name)
    vampytest.assert_instance(output, str)
    return output
