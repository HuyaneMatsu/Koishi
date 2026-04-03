import vampytest

import config

from ..farewell_styles import FAREWELL_STYLE_DEFAULT, FAREWELL_STYLE_FLANDRE, get_farewell_style


def _iter_options():
    yield None, 0, FAREWELL_STYLE_DEFAULT
    yield 'flandre', 0, FAREWELL_STYLE_FLANDRE
    yield None, config.FLANDRE_ID, FAREWELL_STYLE_FLANDRE



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_farewell_style(farewell_style_name, client_id):
    """
    Tests whether ``get_farewell_style`` works as intended.
    
    Parameters
    ----------
    farewell_style_name : `None | str`
        The farewell style's name.
    client_id : ˙int`
        The client's identifier.
    
    returns
    -------
    farewell_style : ``FarewellStyle``
    """
    return get_farewell_style(farewell_style_name, client_id)
