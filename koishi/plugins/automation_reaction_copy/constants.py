__all__ = ()

from hata import BUILTIN_EMOJIS
from hata.ext.slash import Button, Row


CUSTOM_ID_REFRESH = 'reaction_copy.refresh'
CUSTOM_ID_CLOSE = 'reaction_copy.close'

EMOJI_REFRESH = BUILTIN_EMOJIS['arrows_counterclockwise']
EMOJI_CLOSE = BUILTIN_EMOJIS['x']


BUTTON_REFRESH = Button(
    'Refresh',
    EMOJI_REFRESH,
    custom_id = CUSTOM_ID_REFRESH
)
    
BUTTON_CLOSE = Button(
    'Close',
    EMOJI_CLOSE,
    custom_id = CUSTOM_ID_CLOSE,
)

COMPONENTS = Row(BUTTON_REFRESH, BUTTON_CLOSE)
