import vampytest

import config

from ..welcome_styles import WELCOME_STYLE_DEFAULT, WELCOME_STYLE_FLANDRE, get_welcome_style


def _iter_options():
    yield None, 0, WELCOME_STYLE_DEFAULT
    yield 'flandre', 0, WELCOME_STYLE_FLANDRE
    yield None, config.FLANDRE_ID, WELCOME_STYLE_FLANDRE


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_welcome_style(welcome_style_name, client_id):
    """
    Tests whether ``get_welcome_style`` works as intended.
    
    Parameters
    ----------
    welcome_style_name : `None | str`
        The welcome style's name.
    client_id : ˙int`
        The client's identifier.
    
    returns
    -------
    welcome_style : ``WelcomeStyle``
    """
    return get_welcome_style(welcome_style_name, client_id)
