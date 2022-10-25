__all__ = ()

import re

from hata import BUILTIN_EMOJIS, Emoji
from hata.ext.slash import Button


SNIPE_TYPE_EMOJI = 1
SNIPE_TYPE_REACTION = 2
SNIPE_TYPE_STICKER = 3

NAME_BY_SNIPE_TYPE = {
    SNIPE_TYPE_EMOJI: 'emoji',
    SNIPE_TYPE_REACTION: 'reaction',
    SNIPE_TYPE_STICKER: 'sticker',
}

CUSTOM_ID_SNIPE_SELECT_EMOJI = 'snipe.select.emoji'
CUSTOM_ID_SNIPE_SELECT_REACTION = 'snipe.select.reaction'
CUSTOM_ID_SNIPE_SELECT_STICKER = 'snipe.select.sticker'

CUSTOM_ID_SNIPE_INFO_EMOJI = 'snipe.info.emoji'
CUSTOM_ID_SNIPE_INFO_STICKER = 'snipe.ifo.sticker'

CUSTOM_ID_SNIPE_ADD_EMOJI = 'snipe.add.emoji'
CUSTOM_ID_SNIPE_ADD_STICKER = 'snipe.add.sticker'
CUSTOM_ID_SNIPE_ADD_DISABLED = 'snipe.add.disabled'

CUSTOM_ID_SNIPE_DM = 'snipe.dm'
CUSTOM_ID_SNIPE_DM_DISABLED = 'snipe.dm.disabled'

CUSTOM_ID_SNIPE_CLOSE = 'snipe.close'


EMOJI_SNIPE_DM = BUILTIN_EMOJIS['e_mail']
EMOJI_SNIPE_CLOSE = BUILTIN_EMOJIS['x']
EMOJI_SNIPE_INFO = BUILTIN_EMOJIS['notepad_spiral']
EMOJI_SNIPE_ADD = Emoji.precreate(1015148449110433792)


BUTTON_SNIPE_DM = Button(
    'dm me',
    EMOJI_SNIPE_DM,
    custom_id = CUSTOM_ID_SNIPE_DM,
)

BUTTON_SNIPE_DM_DISABLED = Button(
    'dm me',
    EMOJI_SNIPE_DM,
    custom_id = CUSTOM_ID_SNIPE_DM_DISABLED,
    enabled = False,
)

BUTTON_SNIPE_INFO_EMOJI = Button(
    'Show details',
    EMOJI_SNIPE_INFO,
    custom_id = CUSTOM_ID_SNIPE_INFO_EMOJI,
)

BUTTON_SNIPE_INFO_STICKER = Button(
    'Show details',
    EMOJI_SNIPE_INFO,
    custom_id = CUSTOM_ID_SNIPE_INFO_STICKER,
)

BUTTON_SNIPE_ADD_EMOJI = Button(
    'Borrow',
    EMOJI_SNIPE_ADD,
    custom_id = CUSTOM_ID_SNIPE_ADD_EMOJI,
)

BUTTON_SNIPE_ADD_STICKER = Button(
    'Borrow',
    EMOJI_SNIPE_ADD,
    custom_id = CUSTOM_ID_SNIPE_ADD_STICKER,
)

BUTTON_SNIPE_ADD_DISABLED = Button(
    'Borrow',
    EMOJI_SNIPE_ADD,
    custom_id = CUSTOM_ID_SNIPE_ADD_DISABLED,
    enabled = False,
)

BUTTON_SNIPE_CLOSE = Button(
    emoji = EMOJI_SNIPE_CLOSE,
    custom_id = CUSTOM_ID_SNIPE_CLOSE,
)


def create_emoji_add_form_custom_id(emoji):
    return f'snipe.emoji.add.{emoji.id}.{emoji.name}.{emoji.animated:d}'

EMOJI_FORM_PATTERN = re.compile('snipe\.emoji\.add\.(\d+)\.(\w+)\.([01])')


def create_sticker_add_form_custom_id(sticker):
    return f'snipe.sticker.add.{sticker.id}'

STICKER_FORM_PATTERN = re.compile('snipe\.sticker\.add\.(\d+)')
