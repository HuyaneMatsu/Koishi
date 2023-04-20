__all__ = ()

from datetime import timedelta as TimeDelta

from hata import Emoji
from hata.ext.slash import Button, ButtonStyle, Row


EMOJI__KOISHI_THUMBS_UP = Emoji.precreate(945851176128221224)
EMOJI__KOKORO = Emoji.precreate(927881929401974834)


COMPONENT__CONFIRM = Button('Yes', EMOJI__KOISHI_THUMBS_UP, style = ButtonStyle.green, custom_id = 'mod.other.1')
COMPONENT__CANCEL = Button('No', style = ButtonStyle.gray, custom_id = 'mod.other.0')
COMPONENT__ROW = Row(COMPONENT__CONFIRM, COMPONENT__CANCEL)

REGRET_COOLDOWN = 60 * 60 # 1 hour
REGRET_INTERVAL = TimeDelta(hours = 1)
REGRET_INVITE_MAX_AGE = 7 * 24 * 60 * 60 # 1 week

REGRETS = {}
