__all__ = ('get_farewell_style', 'FAREWELL_STYLE_NAMES')

from .flandre import FAREWELL_STYLE as FAREWELL_STYLE_FLANDRE
from .koishi import FAREWELL_STYLE as FAREWELL_STYLE_KOISHI
from .orin import FAREWELL_STYLE as FAREWELL_STYLE_ORIN
from .yoshika import FAREWELL_STYLE as FAREWELL_STYLE_YOSHIKA


FAREWELL_STYLES_BY_NAME = {
    FAREWELL_STYLE_FLANDRE.name: FAREWELL_STYLE_FLANDRE,
    FAREWELL_STYLE_KOISHI.name: FAREWELL_STYLE_KOISHI,
    FAREWELL_STYLE_ORIN.name: FAREWELL_STYLE_ORIN,
    FAREWELL_STYLE_YOSHIKA.name: FAREWELL_STYLE_YOSHIKA,
}


FAREWELL_STYLES_BY_CLIENT_ID = {
    FAREWELL_STYLE_FLANDRE.client_id: FAREWELL_STYLE_FLANDRE,
    FAREWELL_STYLE_KOISHI.client_id: FAREWELL_STYLE_KOISHI,
    FAREWELL_STYLE_ORIN.client_id: FAREWELL_STYLE_ORIN,
    FAREWELL_STYLE_YOSHIKA.client_id: FAREWELL_STYLE_YOSHIKA,
}


FAREWELL_STYLE_DEFAULT = FAREWELL_STYLE_KOISHI


FAREWELL_STYLE_NAMES = sorted(FAREWELL_STYLES_BY_NAME.keys())


def get_farewell_style(farewell_style_name, client_id):
    """
    Gets farewell style for the given name or client identifier.
    
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
    if (farewell_style_name is not None):
        try:
            farewell_style = FAREWELL_STYLES_BY_NAME[farewell_style_name]
        except KeyError:
            pass
        else:
            return farewell_style
    
    try:
        farewell_style = FAREWELL_STYLES_BY_CLIENT_ID[client_id]
    except KeyError:
        pass
    else:
        return farewell_style
    
    
    return FAREWELL_STYLE_DEFAULT
