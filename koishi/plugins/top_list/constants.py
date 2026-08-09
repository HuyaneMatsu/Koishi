__all__ = ()

from hata import AnsiForegroundColor, BUILTIN_EMOJIS, create_ansi_format_code


STYLE_NUMBER = create_ansi_format_code(foreground_color = AnsiForegroundColor.white)
STYLE_VALUE = create_ansi_format_code(foreground_color = AnsiForegroundColor.blue)
STYLE_NAME = create_ansi_format_code(foreground_color = AnsiForegroundColor.white)


PAGE_SIZE = 20


EMOJI_PAGE_PREVIOUS = BUILTIN_EMOJIS['arrow_left']
EMOJI_PAGE_NEXT = BUILTIN_EMOJIS['arrow_right']
EMOJI_CLOSE = BUILTIN_EMOJIS['x']


TOP_LIST_TYPE_BALANCE = 1
TOP_LIST_TYPE_CREDIBILITY = 2
