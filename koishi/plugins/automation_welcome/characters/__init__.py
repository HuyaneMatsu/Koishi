from .koishi import *


__all__ = (
    'WELCOME_DEFAULT',
    'WELCOMES',
    
    *koishi.__all__,
)


from .koishi import IMAGES as KOISHI_IMAGES, MESSAGES as KOISHI_MESSAGES


WELCOMES = {
    'koishi': (KOISHI_MESSAGES, KOISHI_IMAGES),
}

WELCOME_DEFAULT = (KOISHI_MESSAGES, KOISHI_IMAGES)
