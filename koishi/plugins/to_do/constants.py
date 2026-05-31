__all__ = ()

from re import compile as re_compile

from hata import BUILTIN_EMOJIS


ENTRY_BY_ID_RP = re_compile('#(\\d*)\\:?\s*')

PAGE_SIZE = 20

EMOJI_CLOSE = BUILTIN_EMOJIS['x']
EMOJI_PAGE_DECREMENT = BUILTIN_EMOJIS['arrow_left']
EMOJI_PAGE_INCREMENT = BUILTIN_EMOJIS['arrow_right']
