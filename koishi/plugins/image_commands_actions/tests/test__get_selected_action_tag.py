import vampytest

from ..action_filtering import PARAMETER_WILD_CARD, get_selected_action_tag


def _iter_options():
    yield None, None
    yield PARAMETER_WILD_CARD, None
    yield PARAMETER_WILD_CARD.upper(), None
    yield 'fluff', 'fluff'
    yield 'fluff'.upper(), 'fluff'
    yield 'f', 'feed'
    yield 'f'.upper(), 'feed'



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_selected_action_tag(action_tag_name):
    """
    Tests whether ``get_selected_action_tag`` works as intended.
    
    Parameters
    ----------
    action_tag_name : `None | str`
        Action tag name to get action tag for.
    
    Returns
    -------
    output : `None | str`
    """
    output = get_selected_action_tag(action_tag_name)
    vampytest.assert_instance(output, str, nullable = True)
    return output
