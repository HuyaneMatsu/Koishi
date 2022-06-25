__all__ = ()

from hata import BUILTIN_EMOJIS
from hata.ext.slash import Button

CUSTOM_ID_SNIPE_EMOJIS = 'snipe.emoji'
CUSTOM_ID_SNIPE_REACTIONS = 'snipe.reaction'
CUSTOM_ID_SNIPE_STICKERS = 'snipe.sticker'

CUSTOM_ID_SNIPE_EMOJI_INFO = 'snipe.emoji.info'
CUSTOM_ID_SNIPE_STICKER_INFO = 'snipe.sticker.info'

CUSTOM_ID_SNIPE_DM = 'snipe.dm'


EMOJI_SNIPE_DM = BUILTIN_EMOJIS['e_mail']
EMOJI_SNIPE_CLOSE = BUILTIN_EMOJIS['x']
EMOJI_SNIPE_INFO = BUILTIN_EMOJIS['notepad_spiral']

BUTTON_SNIPE_DM = Button('dm me', EMOJI_SNIPE_DM, custom_id=CUSTOM_ID_SNIPE_DM)

BUTTON_SNIPE_EMOJI_INFO = Button('Show details', EMOJI_SNIPE_INFO, custom_id=CUSTOM_ID_SNIPE_EMOJI_INFO)
BUTTON_SNIPE_STICKER_INFO = Button('Show details', EMOJI_SNIPE_INFO, custom_id=CUSTOM_ID_SNIPE_STICKER_INFO)
