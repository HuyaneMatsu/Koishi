__all__ = ()

import re

from hata import BUILTIN_EMOJIS, ButtonStyle, Emoji


SIZE_X = 5
SIZE_Y = 5

SIZE_TOTAL = SIZE_X * SIZE_Y

TILE_VALUE_UNIDENTIFIED = 0
TILE_VALUE_EMPTY = 1
TILE_VALUE_BOMB = 10
TILE_VALUE_FLAG = 11

TILE_UNKNOWN = BUILTIN_EMOJIS['question']
TILE_EMPTY = Emoji.precreate(568838460434284574)

TILE_NEAR_1 = BUILTIN_EMOJIS['one']
TILE_NEAR_2 = BUILTIN_EMOJIS['two']
TILE_NEAR_3 = BUILTIN_EMOJIS['three']
TILE_NEAR_4 = BUILTIN_EMOJIS['four']
TILE_NEAR_5 = BUILTIN_EMOJIS['five']
TILE_NEAR_6 = BUILTIN_EMOJIS['six']
TILE_NEAR_7 = BUILTIN_EMOJIS['seven']
TILE_NEAR_8 = BUILTIN_EMOJIS['eight']

TILE_BOMB = BUILTIN_EMOJIS['bomb']
TILE_FLAG = BUILTIN_EMOJIS['triangular_flag_on_post']


TILES = [
    TILE_UNKNOWN,
    TILE_EMPTY,
    TILE_NEAR_1,
    TILE_NEAR_2,
    TILE_NEAR_3,
    TILE_NEAR_4,
    TILE_NEAR_5,
    TILE_NEAR_6,
    TILE_NEAR_7,
    TILE_NEAR_8,
    TILE_BOMB,
    TILE_FLAG,
]

STYLE_MAP = {
    TILE_VALUE_UNIDENTIFIED: ButtonStyle.gray,
    TILE_VALUE_EMPTY: ButtonStyle.gray,
    TILE_VALUE_BOMB: ButtonStyle.red,
    TILE_VALUE_FLAG: ButtonStyle.green,
}

STYLE_DEFAULT = ButtonStyle.blue


CUSTOM_ID_INITIAL = lambda index, bomb_count: f'ms.i.{index}.{bomb_count}'
CUSTOM_ID_INITIAL_RP = re.compile('ms\\.i\\.(\\d+)\\.(\\d+)')
CUSTOM_ID_CONTINUOUS = lambda index, value : f'ms.c.{index}.{value}'
CUSTOM_ID_CONTINUOUS_RP = re.compile('ms\\.c\\.(\\d+)\\.\\d+')

CONTINUOUS_VALUE_RP = re.compile('ms\\.c\\.\\d+\\.(\\d+)')
