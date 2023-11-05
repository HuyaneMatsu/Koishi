from .koishi import *


__all__ = (
    'WELCOME_STYLE_DEFAULT',
    'WELCOME_STYLES',
    
    *koishi.__all__,
)


from .koishi import WELCOME_STYLE as WELCOME_STYLE_KOISHI


WELCOME_STYLES = {
    WELCOME_STYLE_KOISHI.name: WELCOME_STYLE_KOISHI,
}

WELCOME_STYLE_DEFAULT = WELCOME_STYLE_KOISHI
