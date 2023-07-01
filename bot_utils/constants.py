__all__ = ()

import os
from datetime import datetime as DateTime

from hata import Channel, Color, Emoji, Guild, Invite, Role, User


import config

from config import KOISHI_PATH as PATH__KOISHI
if PATH__KOISHI is None:
    PATH__KOISHI = os.path.abspath('..')

PREFIX__KOISHI = config.KOISHI_PREFIX
PREFIX__SATORI = config.SATORI_PREFIX
PREFIX__FLAN = config.FLAN_PREFIX
PREFIX__MARISA = config.MARISA_PREFIX

GUILD__SUPPORT = Guild.precreate(388267636661682178, name = 'Koishi Wonderland')
GUILD__STORAGE = Guild.precreate(568837922288173056)
GUILD__ESTS_HOME = Guild.precreate(982172577260793866)
GUILD__ORIN_PARTY_HOUSE = Guild.precreate(1082278732850536568)

CHANNEL__SUPPORT__SYSTEM = Channel.precreate(445191707491958784)
CHANNEL__SUPPORT__EVENT = Channel.precreate(798911148292309002)
CHANNEL__SUPPORT__DEFAULT_TEST = Channel.precreate(557187647831932938)
CHANNEL__SUPPORT__LOG_MENTION = Channel.precreate(828552266374053889)
CHANNEL__SUPPORT__LOG_EMOJI = Channel.precreate(864748017726259210)
CHANNEL__SUPPORT__LOG_STICKER = Channel.precreate(864748017726259210)
CHANNEL__SUPPORT__LOG_USER = Channel.precreate(929468601050738688)
CHANNEL__SUPPORT__LOG_SATORI = Channel.precreate(829104265049538620)
CHANNEL__SUPPORT__KOISHI_NEWS = Channel.precreate(1124046720221855835)
CHANNEL__ESTS_HOME__STREAM_NOTIFICATION = Channel.precreate(983676417046904872)
CHANNEL__SYSTEM__SYNC = Channel.precreate(568837922288173058)
CHANNEL__SUPPORT__TOUHOU = Channel.precreate(1023233466634096650)
CHANNEL__SUPPORT__WELCOME = Channel.precreate(445191707491958784)

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
ROLE__ESTS_HOME__STREAM_NOTIFICATION = Role.precreate(983718322753384488)

INVITE__SUPPORT = Invite.precreate('3cH2r5d')

CATEGORY__SUPPORT__BOTS = Channel.precreate(445191611727478795)

EMOJI__HEART_CURRENCY = Emoji.precreate(603533301516599296, name = 'youkai_kokoro')

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

USER__EST = User.precreate(277393805601275910)

DEFAULT_CATEGORY_NAME = 'Uncategorized'

STARTUP = DateTime.utcnow()

IN_GAME_IDS = set()


WAIFU_COST_DEFAULT = 500

WAIFU_SLOT_COST_DEFAULT = 0


"""
y = 0
for x in range(0, 13):
    v = x*x*1000
    y += v
    print(y)
"""


WAIFU_SLOT_2_COST = 5000
WAIFU_SLOT_3_COST = 14000
WAIFU_SLOT_4_COST = 30000
WAIFU_SLOT_5_COST = 55000
WAIFU_SLOT_6_COST = 91000
WAIFU_SLOT_7_COST = 140000
WAIFU_SLOT_8_COST = 204000
WAIFU_SLOT_9_COST = 285000
WAIFU_SLOT_10_COST = 385000
WAIFU_SLOT_11_COST = 506000
WAIFU_SLOT_12_COST = 650000
WAIFU_SLOT_13_COST = 819000
WAIFU_SLOT_14_COST = 1015000
WAIFU_SLOT_15_COST = 1240000
WAIFU_SLOT_16_COST = 1496000
WAIFU_SLOT_17_COST = 1785000
WAIFU_SLOT_18_COST = 2109000
WAIFU_SLOT_19_COST = 2470000
WAIFU_SLOT_20_COST = 2870000

WAIFU_SLOT_COSTS = {
    2: WAIFU_SLOT_2_COST,
    3: WAIFU_SLOT_3_COST,
    4: WAIFU_SLOT_4_COST,
    5: WAIFU_SLOT_5_COST,
    6: WAIFU_SLOT_6_COST,
    7: WAIFU_SLOT_7_COST,
    8: WAIFU_SLOT_8_COST,
    9: WAIFU_SLOT_9_COST,
    10: WAIFU_SLOT_10_COST,
    11: WAIFU_SLOT_11_COST,
    12: WAIFU_SLOT_12_COST,
    13: WAIFU_SLOT_13_COST,
    14: WAIFU_SLOT_14_COST,
    15: WAIFU_SLOT_15_COST,
    16: WAIFU_SLOT_16_COST,
    17: WAIFU_SLOT_17_COST,
    18: WAIFU_SLOT_18_COST,
    19: WAIFU_SLOT_19_COST,
    20: WAIFU_SLOT_20_COST,
}

MAX_WAIFU_SLOTS = 20


KOISHI_HEADER = (
    '```\n'
    ' _   __      _     _     _ \n'
    '| | / /     (_)   | |   (_)\n'
    '| |/ /  ___  _ ___| |__  _ \n'
    '|    \ / _ \| / __| \'_ \| |\n'
    '| |\  \ (_) | \__ \ | | | |\n'
    '\_| \_/\___/|_|___/_| |_|_|\n'
    '```'
)


KOISHI_HEADER_EASTER_EGG = (
    '```\n'
    ' _____ __    ___ \n'
    '|  ___/  |  /   |\n'
    '|___ \`| | / /| |\n'
    '    \ \| |/ /_| |\n'
    '/\__/ /| |\___  |\n'
    '\____/\___/   |_/\n'
    '```'
)
