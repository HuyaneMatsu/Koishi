__all__ = ('get_welcome_style', 'WELCOME_STYLE_NAMES')

import config

from .flandre import WELCOME_STYLE as WELCOME_STYLE_FLANDRE
from .koishi import WELCOME_STYLE as WELCOME_STYLE_KOISHI


WELCOME_STYLES_BY_NAME = {
    WELCOME_STYLE_FLANDRE.name: WELCOME_STYLE_FLANDRE,
    WELCOME_STYLE_KOISHI.name: WELCOME_STYLE_KOISHI,
}


WELCOME_STYLES_BY_CLIENT_ID = {
    config.FLANDRE_ID: WELCOME_STYLE_FLANDRE,
    config.KOISHI_ID: WELCOME_STYLE_KOISHI,
}


WELCOME_STYLE_DEFAULT = WELCOME_STYLE_KOISHI


WELCOME_STYLE_NAMES = sorted(WELCOME_STYLES_BY_NAME.keys())


def get_welcome_style(welcome_style_name, client_id):
    """
    Gets welcome style for the given name or client identifier.
    
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
    if (welcome_style_name is not None):
        try:
            welcome_style = WELCOME_STYLES_BY_NAME[welcome_style_name]
        except KeyError:
            pass
        else:
            return welcome_style
    
    try:
        welcome_style = WELCOME_STYLES_BY_CLIENT_ID[client_id]
    except KeyError:
        pass
    else:
        return welcome_style
    
    
    return WELCOME_STYLE_DEFAULT
