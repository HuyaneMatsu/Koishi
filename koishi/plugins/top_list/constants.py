__all__ = ()

from hata import AnsiForegroundColor, BUILTIN_EMOJIS, create_ansi_format_code
from hata.ext.slash import Button


STYLE_NUMBER = create_ansi_format_code(foreground_color = AnsiForegroundColor.white)
STYLE_HEARTS = create_ansi_format_code(foreground_color = AnsiForegroundColor.blue)
STYLE_NAME = create_ansi_format_code(foreground_color = AnsiForegroundColor.white)


PAGE_SIZE = 20


EMOJI_PAGE_PREVIOUS = BUILTIN_EMOJIS['arrow_left']
EMOJI_PAGE_NEXT = BUILTIN_EMOJIS['arrow_right']
EMOJI_CLOSE = BUILTIN_EMOJIS['x']


CUSTOM_ID_PAGE_BASE = 'top_list.page.'
CUSTOM_ID_PAGE_PREVIOUS_DISABLED = f'{CUSTOM_ID_PAGE_BASE}n-1.disabled'
CUSTOM_ID_PAGE_NEXT_DISABLED = f'{CUSTOM_ID_PAGE_BASE}n+1.disabled'
CUSTOM_ID_CLOSE = 'top_list.close'



BUTTON_PAGE_PREVIOUS_DISABLED = Button(
    'Page 0',
    EMOJI_PAGE_PREVIOUS,
    custom_id = CUSTOM_ID_PAGE_PREVIOUS_DISABLED,
    enabled = False,
)

BUTTON_PAGE_NEXT_DISABLED = Button(
    'Page n',
    EMOJI_PAGE_NEXT,
    custom_id = CUSTOM_ID_PAGE_NEXT_DISABLED,
    enabled = False,
)

BUTTON_CLOSE = Button(
    'Close',
    EMOJI_CLOSE,
    custom_id = CUSTOM_ID_CLOSE,
)
