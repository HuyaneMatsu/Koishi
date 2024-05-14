import vampytest

from ..action_filtering import PARAMETER_WILD_CARD, get_selected_name


def _iter_options():
    yield None, None
    yield PARAMETER_WILD_CARD, None
    yield PARAMETER_WILD_CARD.upper(), None
    yield 'fluff', 'fluff'
    yield 'fluff'.upper(), 'fluff'.casefold()


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_selected_name(parameters):
    """
    Tests whether ``get_selected_name`` works as intended.
    
    Parameters
    ----------
    name : `None | str`
        Image name.
    
    Returns
    -------
    output : `None | str`
    """
    output = get_selected_name(parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return output
