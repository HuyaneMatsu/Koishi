from datetime import datetime
import os
from hata import ChannelText, Guild, Role, Invite, Color, ChannelCategory, Emoji, User


import config

from config import KOISHI_PATH as PATH__KOISHI
if PATH__KOISHI is None:
    PATH__KOISHI = os.path.abspath('..')

PREFIX__KOISHI = config.KOISHI_PREFIX
PREFIX__SATORI = config.SATORI_PREFIX
PREFIX__FLAN = config.FLAN_PREFIX
PREFIX__MARISA = config.MARISA_PREFIX

GUILD__SUPPORT = Guild.precreate(388267636661682178)
GUILD__STORAGE  = Guild.precreate(568837922288173056)

CHANNEL__SUPPORT__SYSTEM = ChannelText.precreate(445191707491958784)
CHANNEL__SUPPORT__EVENT = ChannelText.precreate(798911148292309002)
CHANNEL__SUPPORT__DEFAULT_TEST = ChannelText.precreate(557187647831932938)
CHANNEL__SUPPORT__LOG_MENTION = ChannelText.precreate(828552266374053889)
CHANNEL__SUPPORT__LOG_EMOJI = ChannelText.precreate(864748017726259210)
CHANNEL__SUPPORT__LOG_USER = ChannelText.precreate(929468601050738688)

CHANNEL__SYSTEM__SYNC = ChannelText.precreate(568837922288173058)

ROLE__SUPPORT__VERIFIED = Role.precreate(445189164703678464)
ROLE__SUPPORT__ANNOUNCEMENTS = Role.precreate(538397994421190657)
ROLE__SUPPORT__ELEVATED = Role.precreate(403586901803794432)
ROLE__SUPPORT__BOOSTER = Role.precreate(585556522558554113)
ROLE__SUPPORT__MODERATOR = Role.precreate(726171592509358093)
ROLE__SUPPORT__TESTER = Role.precreate(648138238250319876)
ROLE__SUPPORT__NSFW_ACCESS = Role.precreate(828576094776590377)
ROLE__SUPPORT__EVENT_MANAGER = Role.precreate(798913709019103284)
ROLE__SUPPORT__EVENT_WINNER = Role.precreate(771989284231053323)
ROLE__SUPPORT__EVENT_PARTICIPANT = Role.precreate(801608590720106496)
ROLE__SUPPORT__HEART_BOOST = Role.precreate(846320725580709908)
ROLE__SUPPORT__ADMIN = Role.precreate(403581319139033090)
ROLE__SUPPORT__EMOJI_MANAGER = Role.precreate(864748298116268053)


INVITE__SUPPORT = Invite.precreate('3cH2r5d')

CATEGORY__SUPPORT__BOTS = ChannelCategory.precreate(445191611727478795)
CATEGORY__SUPPORT__BIG_BRO = ChannelCategory.precreate(829104265049538620)

EMOJI__HEART_CURRENCY = Emoji.precreate(603533301516599296, name='youkai_kokoro')

COLOR__SATORI_HELP = Color.from_rgb(118, 0, 161)
COLOR__KOISHI_HELP = Color.from_html('#ffd21e')
COLOR__FLAN_HELP = Color.from_rgb(230, 69, 0)
COLOR__MARISA_HELP = Color.from_html('#e547ed')
COLOR__EVENT = Color(2316923)
COLOR__GAMBLING = Color.from_rgb(254, 254, 164)

LINK__KOISHI_GIT = 'https://github.com/HuyaneMatsu/Koishi'
LINK__HATA_GIT = 'https://github.com/HuyaneMatsu/hata'
LINK__HATA_DOCS = 'https://www.astil.dev/project/hata/docs/hata'
LINK__PASTE = 'https://hastebin.com/'
LINK__HATA_SLASH = 'https://github.com/HuyaneMatsu/hata/blob/master/docs/topics/slash.md'
LINK__KOISHI_TOP_GG = f'https://discordbots.org/bot/{config.KOISHI_ID}'

USER__DISBOARD = User.precreate(302050872383242240, is_bot=True)

DEFAULT_CATEGORY_NAME = 'Uncategorized'

STARTUP = datetime.utcnow()

IN_GAME_IDS = set()
