# Work in progress

import os
from zlib import compress, decompress
from json import load as from_json_file
from math import ceil, floor

from hata import Emoji, Embed, Color, DiscordException, BUILTIN_EMOJIS, Task, WaitTillAll, ERROR_CODES, Client, \
    KOKORO, LOOP_TIME, Lock
from hata.ext.slash import InteractionResponse, abort, Row, Button, ButtonStyle

from sqlalchemy.sql import select

from bot_utils.models import DB_ENGINE, DS_V2_TABLE, ds_v2_model, currency_model, CURRENCY_TABLE, ds_v2_result_model, \
    DS_V2_RESULT_TABLE

from bot_utils.shared import PATH__KOISHI

DS_COLOR             = Color(0xa000c4)
DS_GAMES             = {}
COLOR_TUTORIAL       = Color(0xa000c4)
DIFFICULTY_COLORS    = dict(enumerate((COLOR_TUTORIAL, Color(0x00cc03), Color(0xffe502), Color(0xe50016))))
DIFFICULTY_NAMES     = dict(enumerate(('Tutorial', 'Easy', 'Normal', 'Hard',)))
CHAPTER_UNLOCK_DIFFICULTY = 1
CHAPTER_UNLOCK_STAGE = 10
CHAPTER_UNLOCK_DIFFICULTY_NAME = DIFFICULTY_NAMES[CHAPTER_UNLOCK_DIFFICULTY]
FILE_LOCK            = Lock(KOKORO)
FILE_NAME            = 'ds_v2.json'
FILE_PATH            = os.path.join(PATH__KOISHI, 'library', FILE_NAME)

EMOJI_WEST           = BUILTIN_EMOJIS['arrow_left']
EMOJI_NORTH          = BUILTIN_EMOJIS['arrow_up']
EMOJI_SOUTH          = BUILTIN_EMOJIS['arrow_down']
EMOJI_EAST           = BUILTIN_EMOJIS['arrow_right']

EMOJI_BACK           = BUILTIN_EMOJIS['leftwards_arrow_with_hook']
EMOJI_RESET          = BUILTIN_EMOJIS['arrows_counterclockwise']
EMOJI_CANCEL         = BUILTIN_EMOJIS['x']

EMOJI_UP             = BUILTIN_EMOJIS['arrow_up_small']
EMOJI_DOWN           = BUILTIN_EMOJIS['arrow_down_small']
EMOJI_UP2            = BUILTIN_EMOJIS['arrow_double_up']
EMOJI_DOWN2          = BUILTIN_EMOJIS['arrow_double_down']
EMOJI_LEFT           = BUILTIN_EMOJIS['arrow_backward']
EMOJI_RIGHT          = BUILTIN_EMOJIS['arrow_forward']
EMOJI_SELECT         = BUILTIN_EMOJIS['ok']

EMOJI_NOTHING        = Emoji.precreate(568838460434284574, name='0Q')

EMOJI_REIMU          = Emoji.precreate(574307645347856384, name='REIMU')
EMOJI_FLAN           = Emoji.precreate(575387120147890210, name='FLAN')
EMOJI_YUKARI         = Emoji.precreate(575389643424661505, name='YUKARI')

IDENTIFIER_UP        = '1'
IDENTIFIER_DOWN      = '2'
IDENTIFIER_UP2       = '3'
IDENTIFIER_DOWN2     = '4'
IDENTIFIER_LEFT      = '5'
IDENTIFIER_SELECT    = '6'

IDENTIFIER_WEST      = '7'
IDENTIFIER_NORTH     = '8'
IDENTIFIER_SOUTH     = '9'
IDENTIFIER_EAST      = 'A'

IDENTIFIER_BACK      = 'B'
IDENTIFIER_RESET     = 'C'
IDENTIFIER_CANCEL    = 'D'

IDENTIFIER_EMPTY     = '_'
IDENTIFIER_SKILL     = '0'

BIT_MASK_PASSABLE    = 0b0000000000000111

BIT_MASK_FLOOR       = 0b0000000000000001
BIT_MASK_TARGET      = 0b0000000000000010
BIT_MASK_HOLE_P      = 0b0000000000000011
BIT_MASK_OBJECT_P    = 0b0000000000000100


BIT_MASK_PUSHABLE    = 0b0000000000111000

BIT_MASK_BOX         = 0b0000000000001000
BIT_MASK_BOX_TARGET  = 0b0000000000010000
BIT_MASK_BOX_HOLE    = 0b0000000000011000
BIT_MASK_BOX_OBJECT  = 0b0000000000100000


BIT_MASK_SPECIAL     = 0b0000000011000000

BIT_MASK_HOLE_U      = 0b0000000001000000
BIT_MASK_OBJECT_U    = 0b0000000010000000


BIT_MASK_CHAR        = 0b0000011100000000
BIT_MASK_CHAR_N      = 0b0000010000000000
BIT_MASK_CHAR_E      = 0b0000010100000000
BIT_MASK_CHAR_S      = 0b0000011000000000
BIT_MASK_CHAR_W      = 0b0000011100000000

# BIT_MASK_CN_FLOOR    = 0b0000010000000001
# BIT_MASK_CE_FLOOR    = 0b0000010100000001
# BIT_MASK_CS_FLOOR    = 0b0000011000000001
# BIT_MASK_CW_FLOOR    = 0b0000011100000001
# 
# BIT_MASK_CN_TARGET   = 0b0000010000000010
# BIT_MASK_CE_TARGET   = 0b0000010100000010
# BIT_MASK_CS_TARGET   = 0b0000011000000010
# BIT_MASK_CW_TARGET   = 0b0000011100000010
# 
# BIT_MASK_CN_OBJECT_P = 0b0000010000000011
# BIT_MASK_CE_OBJECT_P = 0b0000010100000011
# BIT_MASK_CS_OBJECT_P = 0b0000011000000011
# BIT_MASK_CW_OBJECT_P = 0b0000011100000011
# 
# BIT_MASK_CN_HOLE_P   = 0b0000010000000100
# BIT_MASK_CE_HOLE_P   = 0b0000010100000100
# BIT_MASK_CS_HOLE_P   = 0b0000011000000100
# BIT_MASK_CW_HOLE_P   = 0b0000011100000100

BIT_MASK_WALL        = 0b1111100000000000

BIT_MASK_NOTHING     = 0b0000100000000000
BIT_MASK_WALL_N      = 0b0001000000000000
BIT_MASK_WALL_E      = 0b0010000000000000
BIT_MASK_WALL_S      = 0b0100000000000000
BIT_MASK_WALL_W      = 0b1000000000000000
# BIT_MASK_WALL_A      = 0b1111000000000000
# BIT_MASK_WALL_SE     = 0b0110000000000000
# BIT_MASK_WALL_SW     = 0b1100000000000000

BIT_MASK_UNPUSHABLE  = BIT_MASK_WALL|BIT_MASK_SPECIAL
BIT_MASK_BLOCKS_LOS  = BIT_MASK_WALL|BIT_MASK_PUSHABLE|BIT_MASK_OBJECT_U

STYLE_DEFAULT_PARTS = {
    BIT_MASK_NOTHING                    : EMOJI_NOTHING.as_emoji,
    BIT_MASK_WALL_E                     : Emoji.precreate(568838488464687169, name='0P').as_emoji,
    BIT_MASK_WALL_S                     : Emoji.precreate(568838546853462035, name='0N').as_emoji,
    BIT_MASK_WALL_W                     : Emoji.precreate(568838580278132746, name='0K').as_emoji,
    BIT_MASK_WALL_N|BIT_MASK_WALL_E|BIT_MASK_WALL_S|BIT_MASK_WALL_W:
                                          Emoji.precreate(578678249518006272, name='0X').as_emoji,
    BIT_MASK_WALL_E|BIT_MASK_WALL_S     : Emoji.precreate(568838557318250499, name='0M').as_emoji,
    BIT_MASK_WALL_S|BIT_MASK_WALL_W     : Emoji.precreate(568838569087598627, name='0L').as_emoji,
    BIT_MASK_WALL_N|BIT_MASK_WALL_E     : Emoji.precreate(574312331849498624, name='01').as_emoji,
    BIT_MASK_WALL_N|BIT_MASK_WALL_W     : Emoji.precreate(574312332453216256, name='00').as_emoji,
    BIT_MASK_WALL_N|BIT_MASK_WALL_E|BIT_MASK_WALL_S:
                                          Emoji.precreate(578648597621506048, name='0R').as_emoji,
    BIT_MASK_WALL_N|BIT_MASK_WALL_S|BIT_MASK_WALL_W:
                                          Emoji.precreate(578648597546139652, name='0S').as_emoji,
    BIT_MASK_WALL_N|BIT_MASK_WALL_S     : Emoji.precreate(578654051848421406, name='0T').as_emoji,
    BIT_MASK_WALL_E|BIT_MASK_WALL_W     : Emoji.precreate(578674409968238613, name='0U').as_emoji,
    BIT_MASK_WALL_N|BIT_MASK_WALL_E|BIT_MASK_WALL_W:
                                          Emoji.precreate(578676096829227027, name='0V').as_emoji,
    BIT_MASK_WALL_E|BIT_MASK_WALL_S|BIT_MASK_WALL_W:
                                          Emoji.precreate(578676650389274646, name='0W').as_emoji,
}

STYLE_REIMU = {**STYLE_DEFAULT_PARTS,
    BIT_MASK_WALL_N                     : Emoji.precreate(580141387631165450, name='0O').as_emoji,
    BIT_MASK_FLOOR                      : Emoji.precreate(574211101638656010, name='0H').as_emoji,
    BIT_MASK_TARGET                     : Emoji.precreate(574234087645249546, name='0A').as_emoji,
    BIT_MASK_OBJECT_P                   : EMOJI_NOTHING.as_emoji,
    BIT_MASK_HOLE_P                     : Emoji.precreate(574202754134835200, name='0I').as_emoji,
    BIT_MASK_BOX                        : Emoji.precreate(574212211434717214, name='0G').as_emoji,
    BIT_MASK_BOX_TARGET                 : Emoji.precreate(574213002190913536, name='0F').as_emoji,
    BIT_MASK_BOX_HOLE                   : Emoji.precreate(574212211434717214, name='0G').as_emoji,
    BIT_MASK_BOX_OBJECT                 : EMOJI_NOTHING.as_emoji,
    BIT_MASK_HOLE_U                     : Emoji.precreate(574187906642477066, name='0J').as_emoji,
    BIT_MASK_OBJECT_U                   : EMOJI_NOTHING.as_emoji,
    BIT_MASK_CHAR_N|BIT_MASK_FLOOR      : Emoji.precreate(574214258871500800, name='0D').as_emoji,
    BIT_MASK_CHAR_E|BIT_MASK_FLOOR      : Emoji.precreate(574213472347226114, name='0E').as_emoji,
    BIT_MASK_CHAR_S|BIT_MASK_FLOOR      : Emoji.precreate(574220751662612502, name='0B').as_emoji,
    BIT_MASK_CHAR_W|BIT_MASK_FLOOR      : Emoji.precreate(574218036156825629, name='0C').as_emoji,
    BIT_MASK_CHAR_N|BIT_MASK_TARGET     : Emoji.precreate(574249292496371732, name='04').as_emoji,
    BIT_MASK_CHAR_E|BIT_MASK_TARGET     : Emoji.precreate(574249292026478595, name='07').as_emoji,
    BIT_MASK_CHAR_S|BIT_MASK_TARGET     : Emoji.precreate(574249292261490690, name='06').as_emoji,
    BIT_MASK_CHAR_W|BIT_MASK_TARGET     : Emoji.precreate(574249292487720970, name='05').as_emoji,
    BIT_MASK_CHAR_N|BIT_MASK_HOLE_P     : Emoji.precreate(574249293662388264, name='02').as_emoji,
    BIT_MASK_CHAR_E|BIT_MASK_HOLE_P     : Emoji.precreate(574249291074240523, name='09').as_emoji,
    BIT_MASK_CHAR_S|BIT_MASK_HOLE_P     : Emoji.precreate(574249291145543681, name='08').as_emoji,
    BIT_MASK_CHAR_W|BIT_MASK_HOLE_P     : Emoji.precreate(574249292957614090, name='03').as_emoji,
    BIT_MASK_CHAR_N|BIT_MASK_OBJECT_P   : EMOJI_NOTHING.as_emoji,
    BIT_MASK_CHAR_E|BIT_MASK_OBJECT_P   : EMOJI_NOTHING.as_emoji,
    BIT_MASK_CHAR_S|BIT_MASK_OBJECT_P   : EMOJI_NOTHING.as_emoji,
    BIT_MASK_CHAR_W|BIT_MASK_OBJECT_P   : EMOJI_NOTHING.as_emoji,
}

STYLE_FLAN = {**STYLE_DEFAULT_PARTS,
    BIT_MASK_WALL_N                     : Emoji.precreate(580143707534262282, name='0X').as_emoji,
    BIT_MASK_FLOOR                      : Emoji.precreate(580150656501940245, name='0Y').as_emoji,
    BIT_MASK_TARGET                     : Emoji.precreate(580153111545511967, name='0b').as_emoji,
    BIT_MASK_OBJECT_P                   : Emoji.precreate(580163014045728818, name='0e').as_emoji,
    BIT_MASK_HOLE_P                     : Emoji.precreate(580159124466303001, name='0d').as_emoji,
    BIT_MASK_BOX                        : Emoji.precreate(580151963937931277, name='0a').as_emoji,
    BIT_MASK_BOX_TARGET                 : Emoji.precreate(580188214086598667, name='0f').as_emoji,
    BIT_MASK_BOX_HOLE                   : Emoji.precreate(580151963937931277, name='0a').as_emoji,
    BIT_MASK_BOX_OBJECT                 : Emoji.precreate(580151963937931277, name='0a').as_emoji,
    BIT_MASK_HOLE_U                     : Emoji.precreate(580156463888990218, name='0c').as_emoji,
    BIT_MASK_OBJECT_U                   : Emoji.precreate(580151385258065925, name='0Z').as_emoji,
    BIT_MASK_CHAR_N|BIT_MASK_FLOOR      : Emoji.precreate(580357693022142485, name='0g').as_emoji,
    BIT_MASK_CHAR_E|BIT_MASK_FLOOR      : Emoji.precreate(580357693093576714, name='0h').as_emoji,
    BIT_MASK_CHAR_S|BIT_MASK_FLOOR      : Emoji.precreate(580357693160685578, name='0i').as_emoji,
    BIT_MASK_CHAR_W|BIT_MASK_FLOOR      : Emoji.precreate(580357693152165900, name='0j').as_emoji,
    BIT_MASK_CHAR_N|BIT_MASK_TARGET     : Emoji.precreate(580357693018210305, name='0k').as_emoji,
    BIT_MASK_CHAR_E|BIT_MASK_TARGET     : Emoji.precreate(580357693085188109, name='0l').as_emoji,
    BIT_MASK_CHAR_S|BIT_MASK_TARGET     : Emoji.precreate(580357693181657089, name='0m').as_emoji,
    BIT_MASK_CHAR_W|BIT_MASK_TARGET     : Emoji.precreate(580357693361881089, name='0n').as_emoji,
    BIT_MASK_CHAR_N|BIT_MASK_HOLE_P     : Emoji.precreate(580357693324132352, name='0o').as_emoji,
    BIT_MASK_CHAR_E|BIT_MASK_HOLE_P     : Emoji.precreate(580357693072736257, name='0p').as_emoji,
    BIT_MASK_CHAR_S|BIT_MASK_HOLE_P     : Emoji.precreate(580357693131456513, name='0q').as_emoji,
    BIT_MASK_CHAR_W|BIT_MASK_HOLE_P     : Emoji.precreate(580357693366337536, name='0r').as_emoji,
    BIT_MASK_CHAR_N|BIT_MASK_OBJECT_P   : Emoji.precreate(580357693143777300, name='0s').as_emoji,
    BIT_MASK_CHAR_E|BIT_MASK_OBJECT_P   : Emoji.precreate(580357692711763973, name='0t').as_emoji,
    BIT_MASK_CHAR_S|BIT_MASK_OBJECT_P   : Emoji.precreate(580357693269606410, name='0u').as_emoji,
    BIT_MASK_CHAR_W|BIT_MASK_OBJECT_P   : Emoji.precreate(580357693387177984, name='0v').as_emoji,
}

STYLE_YUKARI = {**STYLE_DEFAULT_PARTS,
    BIT_MASK_WALL_N                     : Emoji.precreate(593179300270702593, name='0w').as_emoji,
    BIT_MASK_FLOOR                      : Emoji.precreate(593179300426022914, name='0x').as_emoji,
    BIT_MASK_TARGET                     : Emoji.precreate(593179300019306556, name='0y').as_emoji,
    BIT_MASK_OBJECT_P                   : EMOJI_NOTHING.as_emoji,
    BIT_MASK_HOLE_P                     : Emoji.precreate(593179300287479833, name='0z').as_emoji,
    BIT_MASK_BOX                        : Emoji.precreate(593179300296130561, name='10').as_emoji,
    BIT_MASK_BOX_TARGET                 : Emoji.precreate(593179300136615936, name='11').as_emoji,
    BIT_MASK_BOX_HOLE                   : Emoji.precreate(593179300149067790, name='12').as_emoji,
    BIT_MASK_BOX_OBJECT                 : EMOJI_NOTHING.as_emoji,
    BIT_MASK_HOLE_U                     : Emoji.precreate(593179300153262196, name='13').as_emoji,
    BIT_MASK_OBJECT_U                   : EMOJI_NOTHING.as_emoji,
    BIT_MASK_CHAR_N|BIT_MASK_FLOOR      : Emoji.precreate(593179300161650871, name='14').as_emoji,
    BIT_MASK_CHAR_E|BIT_MASK_FLOOR      : Emoji.precreate(593179300153262257, name='15').as_emoji,
    BIT_MASK_CHAR_S|BIT_MASK_FLOOR      : Emoji.precreate(593179300300324887, name='16').as_emoji,
    BIT_MASK_CHAR_W|BIT_MASK_FLOOR      : Emoji.precreate(593179300237410314, name='17').as_emoji,
    BIT_MASK_CHAR_N|BIT_MASK_TARGET     : Emoji.precreate(593179300207919125, name='18').as_emoji,
    BIT_MASK_CHAR_E|BIT_MASK_TARGET     : Emoji.precreate(593179300145135646, name='19').as_emoji,
    BIT_MASK_CHAR_S|BIT_MASK_TARGET     : Emoji.precreate(593179300170301451, name='1A').as_emoji,
    BIT_MASK_CHAR_W|BIT_MASK_TARGET     : Emoji.precreate(593179300153262189, name='1B').as_emoji,
    BIT_MASK_CHAR_N|BIT_MASK_HOLE_P     : Emoji.precreate(593179300199399531, name='1C').as_emoji,
    BIT_MASK_CHAR_E|BIT_MASK_HOLE_P     : Emoji.precreate(593179300300193800, name='1D').as_emoji,
    BIT_MASK_CHAR_S|BIT_MASK_HOLE_P     : Emoji.precreate(593179300216176760, name='1E').as_emoji,
    BIT_MASK_CHAR_W|BIT_MASK_HOLE_P     : Emoji.precreate(593179300153524224, name='1F').as_emoji,
    BIT_MASK_CHAR_N|BIT_MASK_OBJECT_P   : EMOJI_NOTHING.as_emoji,
    BIT_MASK_CHAR_E|BIT_MASK_OBJECT_P   : EMOJI_NOTHING.as_emoji,
    BIT_MASK_CHAR_S|BIT_MASK_OBJECT_P   : EMOJI_NOTHING.as_emoji,
    BIT_MASK_CHAR_W|BIT_MASK_OBJECT_P   : EMOJI_NOTHING.as_emoji,
}

RULES_HELP = Embed('Rules of Dungeon sweeper',
    f'Your quest is to help our cute Touhou characters to put their stuffs on places, where they supposed be. These '
    f'places are marked with an {BUILTIN_EMOJIS["x"]:e} on the floor. Because our characters are lazy, the less steps '
    f'required to sort their stuffs, makes them give you a better rating.\n'
    f'\n'
    f'You can move with the reactions under the embed, to activate your characters\' skill, or go back, reset the map '
    f'or cancel the game:\n'
    f'{EMOJI_WEST:e}{EMOJI_NORTH:e}{EMOJI_SOUTH:e}{EMOJI_EAST:e}{EMOJI_REIMU:e}{EMOJI_BACK:e}'
    f'{EMOJI_RESET:e}{EMOJI_CANCEL:e}\n'
    f'You can show push boxes by moving towards them, but you cannot push more at the same time time or push into the '
    f'wall:\n'
    f'{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_BOX]}{STYLE_REIMU[BIT_MASK_FLOOR]}'
    f'{EMOJI_EAST:e}'
    f'{STYLE_REIMU[BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_BOX]}'
    f'\n'
    f'You can push the boxes into the holes to pass them, but be careful, you might lose too much boxes to finish the '
    f'stages!\n'
    f'{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_BOX]}{STYLE_REIMU[BIT_MASK_HOLE_U]}'
    f'{EMOJI_EAST:e}{STYLE_REIMU[BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}'
    f'{STYLE_REIMU[BIT_MASK_HOLE_P]}{EMOJI_EAST:e}{STYLE_REIMU[BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_FLOOR]}'
    f'{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_HOLE_P]}\n'
    f'{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_BOX]}{STYLE_REIMU[BIT_MASK_HOLE_P]}'
    f'{EMOJI_EAST:e}{STYLE_REIMU[BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}'
    f'{STYLE_REIMU[BIT_MASK_BOX_HOLE]}\n'
    f'If you get a box on the it\'s desired place it\'s color will change:\n'
    f'{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_BOX]}{STYLE_REIMU[BIT_MASK_TARGET]}'
    f'{EMOJI_EAST:e}{STYLE_REIMU[BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}'
    f'{STYLE_REIMU[BIT_MASK_BOX_TARGET]}\n'
    f'The game has 3 chapters. *(there will be more maybe.)* Each chapter introduces a different character to '
    f'play with.',
    color=DS_COLOR,
).add_field(f'Chapter 1 {EMOJI_REIMU:e}',
    f'Your character is Hakurei Reimu (博麗　霊夢), who needs some help at her basement to sort her *boxes* out.\n'
    f'Reimu can jump over a box or hole.\n'
    f'{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_BOX]}{STYLE_REIMU[BIT_MASK_FLOOR]}'
    f'{EMOJI_EAST:e}{STYLE_REIMU[BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_BOX]}'
    f'{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}\n'
    f'{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]:}{STYLE_REIMU[BIT_MASK_HOLE_U]}{STYLE_REIMU[BIT_MASK_FLOOR]}'
    f'{EMOJI_EAST:e}{STYLE_REIMU[BIT_MASK_FLOOR]}{STYLE_REIMU[BIT_MASK_HOLE_U]}'
    f'{STYLE_REIMU[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}'
).add_field(f'Chapter 2 {EMOJI_FLAN:e}',
    f'Your character is Scarlet Flandre (スカーレット・フランドール Sukaaretto Furandooru), who want to put her '
    f'*bookshelves* on their desired place.\n'
    f'Flandre can destroy absolutely anything and everything, and she will get rid of the pillars for you.\n'
    f'{STYLE_FLAN[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}{STYLE_FLAN[BIT_MASK_OBJECT_U]}{EMOJI_EAST:e}'
    f'{STYLE_FLAN[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}{STYLE_FLAN[BIT_MASK_OBJECT_P]}{EMOJI_EAST:e}'
    f'{STYLE_FLAN[BIT_MASK_FLOOR]}{STYLE_FLAN[BIT_MASK_CHAR_E|BIT_MASK_OBJECT_P]}\n'
    f'{STYLE_FLAN[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}{STYLE_FLAN[BIT_MASK_BOX]}{STYLE_FLAN[BIT_MASK_OBJECT_P]}'
    f'{EMOJI_EAST:e}{STYLE_FLAN[BIT_MASK_FLOOR]}{STYLE_FLAN[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}'
    f'{STYLE_FLAN[BIT_MASK_BOX_OBJECT]}'
).add_field(f'Chapter 3 {EMOJI_YUKARI:e}',
    f'Your character is Yakumo Yukari (八雲　紫). Her beddings needs some replacing at her home.\n'
    f'Yukari can create gaps and travel trough them. She will open gap to the closest place straightforward, which is '
    f'separated by a bedding or with wall from her.\n'
    f'{STYLE_YUKARI[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}{STYLE_YUKARI[BIT_MASK_WALL_N]}{STYLE_YUKARI[BIT_MASK_WALL_N]}'
    f'{STYLE_YUKARI[BIT_MASK_FLOOR]}{EMOJI_EAST:e}{STYLE_YUKARI[BIT_MASK_FLOOR]}{STYLE_YUKARI[BIT_MASK_WALL_N]}'
    f'{STYLE_YUKARI[BIT_MASK_WALL_N]}{STYLE_YUKARI[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}\n'
    f'{STYLE_YUKARI[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}{STYLE_YUKARI[BIT_MASK_BOX]}{STYLE_YUKARI[BIT_MASK_BOX]}'
    f'{STYLE_YUKARI[BIT_MASK_FLOOR]}{EMOJI_EAST:e}{STYLE_YUKARI[BIT_MASK_FLOOR]}{STYLE_YUKARI[BIT_MASK_BOX]}'
    f'{STYLE_YUKARI[BIT_MASK_BOX]}{STYLE_YUKARI[BIT_MASK_CHAR_E|BIT_MASK_FLOOR]}'
)

BUTTON_UP_ENABLED = Button(
    emoji = EMOJI_UP,
    custom_id = IDENTIFIER_UP,
    style = ButtonStyle.violet,
)

BUTTON_UP_DISABLED = BUTTON_UP_ENABLED.copy()
BUTTON_UP_DISABLED.enabled = False

BUTTON_DOWN_ENABLED = Button(
    emoji = EMOJI_DOWN,
    custom_id = IDENTIFIER_DOWN,
    style = ButtonStyle.violet,
)

BUTTON_DOWN_DISABLED = BUTTON_DOWN_ENABLED.copy()
BUTTON_DOWN_DISABLED.enabled = False

BUTTON_UP2_ENABLED = Button(
    emoji = EMOJI_UP2,
    custom_id = IDENTIFIER_UP2,
    style = ButtonStyle.violet,
)

BUTTON_UP2_DISABLED = BUTTON_UP2_ENABLED.copy()
BUTTON_UP2_DISABLED.enabled = False

BUTTON_DOWN2_ENABLED = Button(
    emoji = EMOJI_DOWN2,
    custom_id = IDENTIFIER_DOWN2,
    style = ButtonStyle.violet,
)

BUTTON_DOWN2_DISABLED = BUTTON_DOWN2_ENABLED.copy()
BUTTON_DOWN2_DISABLED.enabled = False

BUTTON_LEFT_ENABLED = Button(
    emoji = EMOJI_LEFT,
    custom_id = IDENTIFIER_LEFT,
    style = ButtonStyle.violet,
)

BUTTON_LEFT_DISABLED = BUTTON_LEFT_ENABLED.copy()
BUTTON_LEFT_DISABLED.enabled = False

BUTTON_RIGHT_ENABLED = Button(
    emoji = EMOJI_RIGHT,
    custom_id = EMOJI_RIGHT,
    style = ButtonStyle.violet,
)

BUTTON_RIGHT_DISABLED = BUTTON_RIGHT_ENABLED.copy()
BUTTON_RIGHT_DISABLED.enabled = False

BUTTON_SELECT_ENABLED = Button(
    label =  'Lets go!',
    emoji = EMOJI_SELECT,
    custom_id = IDENTIFIER_SELECT,
    style = ButtonStyle.green,
)

BUTTON_SELECT_DISABLED = BUTTON_SELECT_ENABLED.copy()
BUTTON_SELECT_DISABLED.enabled = False

BUTTON_EMPTY = Button(
    emoji = EMOJI_NOTHING,
    custom_id = IDENTIFIER_EMPTY,
    style = ButtonStyle.gray,
    enabled = False,
)

BUTTON_SKILL_REIMU_ENABLED = Button(
    emoji = EMOJI_REIMU,
    custom_id = IDENTIFIER_SKILL,
    style = ButtonStyle.violet,
)

BUTTON_SKILL_REIMU_DISABLED = BUTTON_SKILL_REIMU_ENABLED.copy()
BUTTON_SKILL_REIMU_DISABLED.enabled = False

BUTTON_SKILL_REIMU_USED = BUTTON_SKILL_REIMU_DISABLED.copy()
BUTTON_SKILL_REIMU_USED.style = ButtonStyle.gray

BUTTON_SKILL_REIMU_ACTIVATED = BUTTON_SKILL_REIMU_ENABLED.copy()
BUTTON_SKILL_REIMU_ACTIVATED.style = ButtonStyle.green

BUTTON_SKILL_FLAN_ENABLED = BUTTON_SKILL_REIMU_ENABLED.copy()
BUTTON_SKILL_FLAN_ENABLED.emoji = EMOJI_FLAN

BUTTON_SKILL_FLAN_DISABLED = BUTTON_SKILL_FLAN_ENABLED.copy()
BUTTON_SKILL_FLAN_DISABLED.enabled = False

BUTTON_SKILL_FLAN_USED = BUTTON_SKILL_FLAN_DISABLED.copy()
BUTTON_SKILL_FLAN_USED.style = ButtonStyle.gray

BUTTON_SKILL_FLAN_ACTIVATED = BUTTON_SKILL_FLAN_ENABLED.copy()
BUTTON_SKILL_FLAN_ACTIVATED.style = ButtonStyle.green

BUTTON_SKILL_YUKARI_ENABLED = BUTTON_SKILL_REIMU_ENABLED.copy()
BUTTON_SKILL_YUKARI_ENABLED.emoji = EMOJI_YUKARI

BUTTON_SKILL_YUKARI_DISABLED = BUTTON_SKILL_YUKARI_ENABLED.copy()
BUTTON_SKILL_YUKARI_DISABLED.enabled = False

BUTTON_SKILL_YUKARI_USED = BUTTON_SKILL_YUKARI_DISABLED.copy()
BUTTON_SKILL_YUKARI_USED.style = ButtonStyle.gray

BUTTON_SKILL_YUKARI_ACTIVATED = BUTTON_SKILL_YUKARI_ENABLED.copy()
BUTTON_SKILL_YUKARI_ACTIVATED.style = ButtonStyle.green

BUTTON_WEST_ENABLED = Button(
    emoji = EMOJI_WEST,
    custom_id = IDENTIFIER_WEST,
    style = ButtonStyle.violet,
)

BUTTON_WEST_DISABLED = BUTTON_WEST_ENABLED.copy()
BUTTON_WEST_DISABLED.enabled = False

BUTTON_NORTH_ENABLED = Button(
    emoji = EMOJI_NORTH,
    custom_id = IDENTIFIER_NORTH,
    style = ButtonStyle.violet,
)

BUTTON_NORTH_DISABLED = BUTTON_NORTH_ENABLED.copy()
BUTTON_NORTH_DISABLED.enabled = False

BUTTON_SOUTH_ENABLED = Button(
    emoji = EMOJI_SOUTH,
    custom_id = IDENTIFIER_SOUTH,
    style = ButtonStyle.violet,
)

BUTTON_SOUTH_DISABLED = BUTTON_SOUTH_ENABLED.copy()
BUTTON_SOUTH_DISABLED.enabled = False

BUTTON_EAST_ENABLED = Button(
    emoji = EMOJI_EAST,
    custom_id = IDENTIFIER_EAST,
    style = ButtonStyle.violet,
)

BUTTON_EAST_DISABLED = BUTTON_EAST_ENABLED.copy()
BUTTON_EAST_DISABLED.enabled = False

BUTTON_BACK_ENABLED = Button(
    emoji = EMOJI_BACK,
    custom_id = IDENTIFIER_BACK,
    style = ButtonStyle.violet,
)

BUTTON_BACK_DISABLED = BUTTON_BACK_ENABLED.copy()
BUTTON_BACK_DISABLED.enabled = False

BUTTON_RESET_ENABLED = Button(
    emoji = EMOJI_RESET,
    custom_id = IDENTIFIER_RESET,
    style = ButtonStyle.violet,
)

BUTTON_RESET_DISABLED = BUTTON_RESET_ENABLED.copy()
BUTTON_RESET_DISABLED.enabled = False

BUTTON_CANCEL = Button(
    emoji = EMOJI_CANCEL,
    custom_id = IDENTIFIER_CANCEL,
    style = ButtonStyle.red,
)


def get_rating_for(stage, best):
    stage_best = stage.best
    rating_difference = floor(stage.best/20.0)+5.0
    
    for rating in ('S', 'A', 'B', 'C', 'D', 'E'):
        if best <= stage_best:
            break
        
        stage_best += rating_difference
    
    return rating

class MoveDirectories:
    __slots__ = ('north', 'east', 'south', 'west')

SKILL_DIRECTORY_DESCRIPTORS = (
    MoveDirectories.north.__set__,
    MoveDirectories.east.__set__,
    MoveDirectories.south.__set__,
    MoveDirectories.west.__set__,
)


def REIMU_SKILL_CAN_ACTIVATE(self):
    x_size = self.source.x_size
    position = self.position
    map_ = self.map
    
    for step in (-x_size, 1, x_size, -1):
        target_tile=map_[position+step]
        
        if not target_tile&(BIT_MASK_PUSHABLE|BIT_MASK_SPECIAL):
            continue
        
        after_tile = map_[position+(step<<1)]

        if not after_tile&BIT_MASK_PASSABLE:
            continue
        
        return True
    
    return False


def REIMU_SKILL_GET_DIRECTORIES(self):
    x_size = self.source.x_size
    position = self.position
    map_ = self.map
    
    move_directories = MoveDirectories()
    
    for step, descriptor in zip((-x_size, 1, x_size, -1), SKILL_DIRECTORY_DESCRIPTORS):
        target_tile = map_[position+step]
        
        if target_tile&(BIT_MASK_PUSHABLE|BIT_MASK_SPECIAL):
            after_tile = map_[position+(step<<1)]
    
            if after_tile&BIT_MASK_PASSABLE:
                can_go_to_directory = True
            else:
                can_go_to_directory = False
        else:
            can_go_to_directory = False
        
        descriptor(move_directories, can_go_to_directory)
    
    return move_directories


def REIMU_SKILL_USE(self, step, align):
    map_ = self.map
    position = self.position
    
    target_tile = map_[position+step]
    
    if not target_tile&(BIT_MASK_PUSHABLE|BIT_MASK_SPECIAL):
        return False
    
    after_tile = map_[position+(step<<1)]
    
    if not after_tile&BIT_MASK_PASSABLE:
        return False
    
    actual_tile = map_[position]
    self.history.append(HistoryElement(position, True, ((position, actual_tile), (position+(step<<1), after_tile))))
    
    map_[position] = actual_tile&BIT_MASK_PASSABLE
    self.position = position = position+(step<<1)
    
    map_[position] = after_tile|align
    self.has_skill = False
    
    return True


def FLAN_SKILL_CAN_ACTIVATE(self):
    x_size = self.source.x_size
    position = self.position
    map_ = self.map
    
    for step in (-x_size, 1, x_size, -1):
        target_tile = map_[position+step]
        
        if target_tile == BIT_MASK_OBJECT_U:
            return True
    
    return False


def FLAN_SKILL_GET_DIRECTORIES(self):
    x_size = self.source.x_size
    position = self.position
    map_ = self.map
    
    move_directories = MoveDirectories()
    
    for step, descriptor in zip((-x_size, 1, x_size, -1), SKILL_DIRECTORY_DESCRIPTORS):
        target_tile = map_[position+step]
        if target_tile == BIT_MASK_OBJECT_U:
            can_go_to_directory = True
        else:
            can_go_to_directory = False
        
        descriptor(move_directories, can_go_to_directory)
    
    return move_directories


def FLAN_SKILL_USE(self, step, align):
    map_ = self.map
    position = self.position
    
    target_tile = map_[position+step]
    
    if target_tile != BIT_MASK_OBJECT_U:
        return False
    
    actual_tile = map_[position]
    self.history.append(HistoryElement(position, True, ((position, actual_tile), (position+step, target_tile))))
    
    map_[position] = actual_tile&BIT_MASK_PASSABLE|align
    map_[position+step] = BIT_MASK_OBJECT_P
    self.has_skill = False
    
    return True


def YUKARI_SKILL_CAN_ACTIVATE(self):
    map_ = self.map
    
    x_size = self.source.x_size
    y_size = len(map_)//x_size

    position = self.position
    y_position, x_position = divmod(position, x_size)

    # x_min = x_size*y_position
    # x_max = x_size*(y_position+1)-1
    # y_min = x_position
    # y_max = x_position+(x_size*(y_size-1))
    
    for step, limit in (
            (-x_size , -x_size                       ,),
            (1       , x_size*(y_position+1)-1       ,),
            (x_size  , x_position+(x_size*(y_size-1)),),
            (-1      , x_size*y_position             ,),
                 ):
        target_position = position+step
        if target_position == limit:
            continue
        
        if not map_[target_position]&BIT_MASK_BLOCKS_LOS:
            continue
        
        while True:
            target_position = target_position+step
            if target_position == limit:
                break
            
            target_tile = map_[target_position]
            if target_tile&BIT_MASK_BLOCKS_LOS:
                continue
            
            if target_tile&BIT_MASK_PASSABLE:
                return True
            
            break
    
    return False

def YUKARI_SKILL_GET_DIRECTORIES(self):
    map_ = self.map
    
    x_size = self.source.x_size
    y_size = len(map_)//x_size
    
    move_directories = MoveDirectories()
    
    position = self.position
    y_position, x_position = divmod(position, x_size)

    # x_min = x_size*y_position
    # x_max = x_size*(y_position+1)-1
    # y_min = x_position
    # y_max = x_position+(x_size*(y_size-1))
    
    for (step, limit), descriptor in zip((
            (-x_size , -x_size                       ,),
            (1       , x_size*(y_position+1)-1       ,),
            (x_size  , x_position+(x_size*(y_size-1)),),
            (-1      , x_size*y_position             ,),
                 ), SKILL_DIRECTORY_DESCRIPTORS):
        
        target_position = position+step
        if target_position == limit:
            can_go_to_directory = False
        else:
            if map_[target_position]&BIT_MASK_BLOCKS_LOS:
                while True:
                    target_position = target_position+step
                    if target_position == limit:
                        can_go_to_directory = False
                        break
                    
                    target_tile = map_[target_position]
                    if target_tile&BIT_MASK_BLOCKS_LOS:
                        continue
                    
                    if target_tile&BIT_MASK_PASSABLE:
                        can_go_to_directory = True
                        break
                    
                    can_go_to_directory = False
                    break
            else:
                can_go_to_directory = False
        
        descriptor(move_directories, can_go_to_directory)
    
    return move_directories


def YUKARI_SKILL_USE(self, step, align):
    map_ = self.map

    x_size = self.source.x_size
    y_size = len(map_)//x_size
    
    position = self.position
    y_position, x_position = divmod(position, x_size)

    if step > 0:
        if step == 1:
            limit = x_size*(y_position+1)-1
        else:
            limit = x_position+(x_size*(y_size-1))
    else:
        if step == -1:
            limit = x_size*y_position
        else:
            limit = -x_size

    target_position = position+step
    
    if target_position == limit:
        return False
    
    if not map_[target_position]&BIT_MASK_BLOCKS_LOS:
        return False
    
    while True:
        target_position = target_position+step
        if target_position == limit:
            return False
        
        target_tile = map_[target_position]
        if target_tile&BIT_MASK_BLOCKS_LOS:
            continue
        
        if target_tile&BIT_MASK_PASSABLE:
            break
        
        return False
    
    actual_tile = map_[position]
    self.history.append(HistoryElement(position, True, ((position, actual_tile), (target_position, target_tile))))
    
    map_[position] = actual_tile&BIT_MASK_PASSABLE
    self.position = target_position
    
    map_[target_position] = target_tile|align
    self.has_skill = False
    
    return True


class HistoryElement:
    __slots__ = ('changes', 'position', 'was_skill')
    
    def __init__(self, position, was_skill, changes):
        self.position = position
        self.was_skill = was_skill
        self.changes = changes
    
    @classmethod
    def from_json(cls, data):
        self = object.__new__(cls)
        self.position = data[JSON_KEY_HISTORY_ELEMENT_POSITION]
        self.was_skill = data[JSON_KEY_HISTORY_ELEMENT_WAS_SKILL]
        self.changes = tuple(tuple(change) for change in data[JSON_KEY_HISTORY_ELEMENT_CHANGES])
        return self
    
    def to_json(self):
        return {
            JSON_KEY_HISTORY_ELEMENT_POSITION: self.position,
            JSON_KEY_HISTORY_ELEMENT_WAS_SKILL: self.was_skill,
            JSON_KEY_HISTORY_ELEMENT_CHANGES: self.changes,
        }


TILE_NAME_TO_VALUE = {
    'FLOOR'     : BIT_MASK_FLOOR,
    'TARGET'    : BIT_MASK_TARGET,
    'BOX'       : BIT_MASK_BOX,
    'BOX_TARGET': BIT_MASK_BOX_TARGET,
    'HOLE_U'    : BIT_MASK_HOLE_U,
    'HOLE_P'    : BIT_MASK_HOLE_P,
    'OBJECT_U'  : BIT_MASK_OBJECT_U,
    'CN_FLOOR'  : BIT_MASK_CHAR_N|BIT_MASK_FLOOR,
    'CE_FLOOR'  : BIT_MASK_CHAR_E|BIT_MASK_FLOOR,
    'CS_FLOOR'  : BIT_MASK_CHAR_S|BIT_MASK_FLOOR,
    'CW_FLOOR'  : BIT_MASK_CHAR_W|BIT_MASK_FLOOR,
    'NOTHING'   : BIT_MASK_NOTHING,
    'WALL_N'    : BIT_MASK_WALL_N,
    'WALL_E'    : BIT_MASK_WALL_E,
    'WALL_S'    : BIT_MASK_WALL_S,
    'WALL_W'    : BIT_MASK_WALL_W,
    'WALL_HV'   : BIT_MASK_WALL_N|BIT_MASK_WALL_E|BIT_MASK_WALL_S|BIT_MASK_WALL_W,
    'WALL_SE'   : BIT_MASK_WALL_E|BIT_MASK_WALL_S,
    'WALL_SW'   : BIT_MASK_WALL_S|BIT_MASK_WALL_W,
    'WALL_NE'   : BIT_MASK_WALL_N|BIT_MASK_WALL_E,
    'WALL_NW'   : BIT_MASK_WALL_N|BIT_MASK_WALL_W,
    'WALL_HE'   : BIT_MASK_WALL_N|BIT_MASK_WALL_E|BIT_MASK_WALL_S,
    'WALL_HW'   : BIT_MASK_WALL_N|BIT_MASK_WALL_S|BIT_MASK_WALL_W,
    'WALL_H'    : BIT_MASK_WALL_N|BIT_MASK_WALL_S,
    'CN_TARGET' : BIT_MASK_CHAR_N|BIT_MASK_TARGET,
    'CE_TARGET' : BIT_MASK_CHAR_E|BIT_MASK_TARGET,
    'CS_TARGET' : BIT_MASK_CHAR_S|BIT_MASK_TARGET,
    'CW_TARGET' : BIT_MASK_CHAR_W|BIT_MASK_TARGET,
    'WALL_V'    : BIT_MASK_WALL_E|BIT_MASK_WALL_W,
    'WALL_NV'   : BIT_MASK_WALL_E|BIT_MASK_WALL_S|BIT_MASK_WALL_W,
    'WALL_SV'   : BIT_MASK_WALL_N|BIT_MASK_WALL_E|BIT_MASK_WALL_W,
}

TILE_VALUE_TO_NAME = {value: key for key, value in TILE_NAME_TO_VALUE.items()}

JSON_KEY_STAGE_SOURCE_BEST = 'b'
JSON_KEY_STAGE_SOURCE_CHAPTER_INDEX = 'c'
JSON_KEY_STAGE_SOURCE_DIFFICULTY_INDEX = 'd'
JSON_KEY_STAGE_SOURCE_STAGE_INDEX = 's'
JSON_KEY_STAGE_SOURCE_ID = 'i'
JSON_KEY_STAGE_SOURCE_START = 'p'
JSON_KEY_STAGE_SOURCE_TARGET_COUNT = 't'
JSON_KEY_STAGE_SOURCE_MAP = 'm'
JSON_KEY_STAGE_X_SIZE = 'x'

JSON_KEY_HISTORY_ELEMENT_POSITION = '0'
JSON_KEY_HISTORY_ELEMENT_WAS_SKILL = '1'
JSON_KEY_HISTORY_ELEMENT_CHANGES = '2'

JSON_KEY_GAME_STATE_SOURCE = '0'
JSON_KEY_GAME_STATE_MAP = '1'
JSON_KEY_GAME_STATE_POSITION = '2'
JSON_KEY_GAME_STATE_HAS_SKILL = '3'
JSON_KEY_GAME_STATE_NEXT_SKILL = '4'
JSON_KEY_GAME_STATE_HISTORY = '5'

STAGES_BY_ID = {}

class StageSource:
    __slots__ = ('best', 'chapter_index', 'difficulty_index', 'stage_index', 'id', 'start', 'target_count', 'map',
        'x_size')
    
    @classmethod
    def from_json(cls, data):
        self = object.__new__(cls)
        self.best = data[JSON_KEY_STAGE_SOURCE_BEST]
        self.chapter_index = data[JSON_KEY_STAGE_SOURCE_CHAPTER_INDEX]
        self.difficulty_index = data[JSON_KEY_STAGE_SOURCE_DIFFICULTY_INDEX]
        self.stage_index = data[JSON_KEY_STAGE_SOURCE_STAGE_INDEX]
        identifier = data[JSON_KEY_STAGE_SOURCE_ID]
        self.id = identifier
        self.start = data[JSON_KEY_STAGE_SOURCE_START]
        self.target_count = data[JSON_KEY_STAGE_SOURCE_TARGET_COUNT]
        self.map = [TILE_NAME_TO_VALUE[tile_name] for tile_name in data[JSON_KEY_STAGE_SOURCE_MAP]]
        self.x_size = data[JSON_KEY_STAGE_X_SIZE]
        
        STAGES_BY_ID[self.id] = self
        
        return self


def pretty_dump_stage_sources(stage_sources):
    json_parts = []
    
    json_parts.append('[\n')
    
    is_first = True
    
    for stage_source in stage_sources:
        if is_first:
            json_parts.append(' '*4)
            is_first = False
        else:
            json_parts.append(' ')
        
        json_parts.append('{')
        json_parts.append(' '*8)
        json_parts.append('\n')
        
        json_parts.append(' '*8)
        json_parts.append('"')
        json_parts.append(JSON_KEY_STAGE_SOURCE_CHAPTER_INDEX)
        json_parts.append('": ')
        json_parts.append(stage_source.chapter_index)
        json_parts.append(',\n')
        json_parts.append(' '*8)
        json_parts.append('"')
        json_parts.append(JSON_KEY_STAGE_SOURCE_DIFFICULTY_INDEX)
        json_parts.append('": ')
        json_parts.append(repr(stage_source.difficulty_index))
        json_parts.append(',\n')
        json_parts.append(' '*8)
        json_parts.append('"')
        json_parts.append(JSON_KEY_STAGE_SOURCE_STAGE_INDEX)
        json_parts.append('": ')
        json_parts.append(repr(stage_source.stage_index))
        json_parts.append(',\n')
        json_parts.append(' '*8)
        json_parts.append('"')
        json_parts.append(JSON_KEY_STAGE_SOURCE_ID)
        json_parts.append('": ')
        json_parts.append(repr(stage_source.id))
        json_parts.append(',\n')
        json_parts.append(' '*8)
        json_parts.append('"')
        json_parts.append(JSON_KEY_STAGE_SOURCE_START)
        json_parts.append('": ')
        json_parts.append(repr(stage_source.start))
        json_parts.append(',\n')
        json_parts.append(' '*8)
        json_parts.append('"')
        json_parts.append(JSON_KEY_STAGE_SOURCE_TARGET_COUNT)
        json_parts.append('": ')
        json_parts.append(repr(stage_source.target_count))
        json_parts.append(',\n')
        json_parts.append(' '*8)
        json_parts.append('"')
        json_parts.append(JSON_KEY_STAGE_X_SIZE)
        json_parts.append('": ')
        json_parts.append(repr(stage_source.x_size))
        json_parts.append(',\n')
        json_parts.append(' '*8)
        json_parts.append('"')
        json_parts.append(JSON_KEY_STAGE_SOURCE_BEST)
        json_parts.append('": ')
        json_parts.append(repr(999))
        json_parts.append(',\n')
        json_parts.append(' '*8)
        json_parts.append('"')
        json_parts.append(JSON_KEY_STAGE_SOURCE_MAP)
        json_parts.append('": [\n')
        
        map_ = stage_source.map
        map_.reverse()
        while map_:
            is_first_in_line = True
            for _ in range(stage_source.x_size):
                tile_value = map_.pop()
                tile_name = TILE_VALUE_TO_NAME[tile_value]
                
                if is_first_in_line:
                    is_first_in_line = False
                else:
                    json_parts.append(' ')
                
                json_parts.append('"')
                json_parts.append(tile_name)
                json_parts.append('"')
                json_parts.append(' '*(10-len(tile_name)))
                json_parts.append(',')
            
            json_parts.append('\n')
        
        if (json_parts[-1] == '\n') and (json_parts[-2] == ','):
            del json_parts[-2]
        
        json_parts.append(' '*8)
        json_parts.append(']\n')
        json_parts.append(' '*4)
        json_parts.append('}')
        json_parts.append(',')
    
    if json_parts[-1] == ',':
        del json_parts[-1]
    
    json_parts.append('\n]\n')
    
    return ''.join(json_parts)

CHAPTER_REIMU_NAME = 'REIMU'
CHAPTER_FLAN_NAME = 'FLAN'
CHAPTER_YUKARI_NAME = 'YUKARI'

CHAPTER_REIMU_INDEX = 0
CHAPTER_FLAN_INDEX = 1
CHAPTER_YUKARI_INDEX = 2

CHAPTER_NAME_TO_INDEX = {
    CHAPTER_REIMU_NAME: CHAPTER_REIMU_INDEX,
    CHAPTER_FLAN_NAME: CHAPTER_FLAN_INDEX,
    CHAPTER_YUKARI_INDEX: CHAPTER_YUKARI_INDEX,
}

CHAPTERS = {}

class Chapter:
    __slots__ = ('button_skill_disabled', 'button_skill_enabled', 'button_skill_used', 'difficulties', 'emoji',
        'identifier', 'button_skill_activated', 'skill_can_active', 'skill_get_directories', 'skill_use', 'style',
        'stages_sorted',)
    def __init__(self, identifier, emoji, style, button_skill_enabled, button_skill_disabled, button_skill_used,
            button_skill_activated, skill_can_active, skill_get_directories, skill_use):
        self.identifier = identifier
        self.difficulties = None
        self.stages_sorted = []
        self.emoji = emoji
        self.style = style
        self.button_skill_enabled = button_skill_enabled
        self.button_skill_disabled = button_skill_disabled
        self.button_skill_used = button_skill_used
        self.button_skill_activated = button_skill_activated
        self.skill_can_active = skill_can_active
        self.skill_get_directories = skill_get_directories
        self.skill_use = skill_use

CHAPTERS[CHAPTER_REIMU_INDEX] = Chapter(
    CHAPTER_REIMU_INDEX,
    EMOJI_REIMU,
    STYLE_REIMU,
    BUTTON_SKILL_REIMU_ENABLED,
    BUTTON_SKILL_REIMU_DISABLED,
    BUTTON_SKILL_REIMU_USED,
    BUTTON_SKILL_REIMU_ACTIVATED,
    REIMU_SKILL_CAN_ACTIVATE,
    REIMU_SKILL_GET_DIRECTORIES,
    REIMU_SKILL_USE,
)

CHAPTERS[CHAPTER_FLAN_INDEX] = Chapter(
    CHAPTER_FLAN_INDEX,
    EMOJI_FLAN,
    STYLE_FLAN,
    BUTTON_SKILL_FLAN_ENABLED,
    BUTTON_SKILL_FLAN_DISABLED,
    BUTTON_SKILL_FLAN_USED,
    BUTTON_SKILL_FLAN_ACTIVATED,
    FLAN_SKILL_CAN_ACTIVATE,
    FLAN_SKILL_GET_DIRECTORIES,
    FLAN_SKILL_USE,
)

CHAPTERS[CHAPTER_YUKARI_INDEX] = Chapter(
    CHAPTER_YUKARI_INDEX,
    EMOJI_YUKARI,
    STYLE_YUKARI,
    BUTTON_SKILL_YUKARI_ENABLED,
    BUTTON_SKILL_YUKARI_DISABLED,
    BUTTON_SKILL_YUKARI_USED,
    BUTTON_SKILL_YUKARI_ACTIVATED,
    YUKARI_SKILL_CAN_ACTIVATE,
    YUKARI_SKILL_GET_DIRECTORIES,
    YUKARI_SKILL_USE,
)


def load_stages():
    stage_source_datas = from_json_file(FILE_PATH)
    stage_sources = []
    for stage_source_data in stage_source_datas:
        stage_source = StageSource.from_json(stage_source_data)
        stage_sources.append(stage_source)
    
    chapters = {}
    for stage_source in stage_sources:
        try:
            chapter = chapters[stage_source.chapter_index]
        except KeyError:
            chapter = chapters[stage_source.chapter_index] = {}
        
        try:
            difficulty = chapter[stage_source.difficulty_index]
        except KeyError:
            difficulty = chapter[stage_source.difficulty_index] = {}
        
        difficulty[stage_source.stage_index] = stage_source
    
    sorted_chapters = []
    for expected_chapter_index, (chapter_index, chapter) in enumerate(sorted(chapters.items())):
        if expected_chapter_index != chapter_index:
            raise RuntimeError(
                f'expected_chapter_index={expected_chapter_index!r} != '
                f'chapter_index={chapter_index!r})'
            )
        
        if chapter_index not in CHAPTERS:
            raise RuntimeError(
                f'chapter_index={chapter_index} not in '
                f'CHAPTERS={CHAPTERS}'
            )
        
        sorted_difficulty = []
        sorted_chapters.append(sorted_difficulty)
        
        for expected_difficulty_index, (difficulty_index, difficulty) in enumerate(sorted(chapter.items())):
            if expected_difficulty_index != difficulty_index:
                raise RuntimeError(
                    f'expected_difficulty_index={expected_difficulty_index!r} != '
                    f'difficulty_index={difficulty_index!r})'
                )
                
            sorted_stages = []
            sorted_difficulty.append(sorted_stages)
            for expected_stage_index, (stage_index, stage) in enumerate(sorted(difficulty.items())):
                if expected_difficulty_index != difficulty_index:
                    raise RuntimeError(
                        f'expected_stage_index={expected_stage_index!r} != '
                        f'stage_index={stage_index!r})'
                    )
                    
                sorted_stages.append(stage)
    
    for chapter_index, chapter in enumerate(sorted_chapters):
        chapter_object = CHAPTERS[chapter_index]
        chapter_object.difficulties = chapters[chapter_index]
        for difficulty in chapter:
            chapter_object.stages_sorted.extend(difficulty)


load_stages()


class StageState:
    __slots__ = ('id', 'stage_id', 'best')
    
    def __new__(cls, field):
        self = object.__new__(cls)
        self.id = field.id
        self.stage_id = field.stage_id
        self.best = field.best
        return self


class UserState:
    __slots__ = ('game_state', 'stage_results', 'entry_id', 'field_exists', 'selected_chapter_index',
        'selected_stage_index', 'selected_difficulty_index', 'user_id',)
    
    async def __new__(cls, user_id):
        async with DB_ENGINE.connect() as connector:
            response = await connector.execute(
                DS_V2_TABLE. \
                    select(ds_v2_model.user_id==user_id)
            )
            results = await response.fetchall()
            
            if results:
                result = results[0]
                game_state_data = result.game_state
                if (game_state_data is None):
                    game_state = None
                else:
                    game_state_json_data = decompress(game_state_data)
                    game_state = GameState.from_json(game_state_json_data)
                
                selected_chapter_index = result.selected_chapter_index
                selected_stage_index = result.selected_stage_index
                selected_difficulty_index = result.selected_difficulty_index
                field_exists = True
                entry_id = result.id
                
                response = await connector.execute(
                    DS_V2_RESULT_TABLE. \
                    select(ds_v2_result_model.ds_v2_entry_id==entry_id)
                )
                
                results = await response.fetchall()
                
                stage_results = {}
                for result in results:
                    stage_state = StageState(result)
                    stage_results[stage_state.stage_id] = stage_results
            else:
                game_state = None
                stage_results = {}
                selected_chapter_index = 0
                selected_stage_index = 0
                selected_difficulty_index = 0
                field_exists = False
                entry_id = 0
        
        self = object.__new__(cls)
        self.game_state = game_state
        self.selected_chapter_index = selected_chapter_index
        self.selected_stage_index = selected_stage_index
        self.selected_difficulty_index = selected_difficulty_index
        self.field_exists = field_exists
        self.entry_id = entry_id
        self.stage_results = stage_results
    
    
    def get_game_state_data(self):
        game_state = self.game_state
        if (game_state is None):
            game_state_data = None
        else:
            game_state_json_data = game_state.to_json()
            game_state_data = compress(game_state_json_data)
        
        return game_state_data
    
    async def upload(self):
        game_state_data = self.get_game_state_data()
        
        async with DB_ENGINE.connect() as connector:
            if self.field_exists:
                await connector.execute(
                    DS_V2_TABLE.update(). \
                    values(
                        game_state                = game_state_data,
                        selected_chapter_index    = self.selected_chapter_index,
                        selected_stage_index      = self.selected_stage_index,
                        selected_difficulty_index = self.selected_difficulty_index,
                    ).where(ds_v2_model.id==self.entry_id)
                )
            else:
                response = await connector.execute(
                    DS_V2_TABLE.insert(). \
                    values(
                        user_id                   = self.user_id,
                        game_state                = game_state_data,
                        selected_chapter_index    = self.selected_chapter_index,
                        selected_stage_index      = self.selected_stage_index,
                        selected_difficulty_index = self.selected_difficulty_index,
                    ). \
                    returning(ds_v2_model.id)
                )
                result = await response.fetchone()
                self.entry_id = result[0]
                self.field_exists = True
    
    async def set_best(self, stage_id, best):
        if not self.field_exists:
            async with DB_ENGINE.connect() as connector:
                game_state_data = self.get_game_state_data()
                
                await connector.execute(
                    DS_V2_TABLE.insert(). \
                    values(
                        user_id                   = self.user_id,
                        game_state                = game_state_data,
                        selected_chapter_index    = self.selected_chapter_index,
                        selected_stage_index      = self.selected_stage_index,
                        selected_difficulty_index = self.selected_difficulty_index,
                    )
                )
            
            self.field_exists = True
        
class GameState:
    __slots__ = ('best', 'chapter', 'has_skill', 'history', 'map', 'next_skill', 'position', 'source',)
    
    def __init__(self, chapter, source, best):
        self.chapter = chapter
        self.source = source
        self.map = source.map.copy()
        self.position = source.start
        self.history = []
        self.has_skill = True
        self.next_skill = False
        self.best = best
    
    
    @classmethod
    def from_json(cls, data):
        self = object.__new__(cls)
        
        chapter_identifier, difficulty_identifier, stage_identifier, best = data[JSON_KEY_GAME_STATE_SOURCE]
        
        chapter = CHAPTERS[chapter_identifier]
        self.chapter = chapter
        source = chapter.difficulties[difficulty_identifier][stage_identifier]
        self.source = source
        self.best = best
        
        try:
            map_ = data[JSON_KEY_GAME_STATE_MAP]
        except KeyError:
            map_ = source.map.copy()
        
        self.map = map_
        
        try:
            position = data[JSON_KEY_GAME_STATE_POSITION]
        except KeyError:
            position = source.start
        
        self.position = position
        
        self.has_skill = data.get(JSON_KEY_GAME_STATE_HAS_SKILL, True)
        self.next_skill = data.get(JSON_KEY_GAME_STATE_NEXT_SKILL, True)
        
        try:
            history_datas = data[JSON_KEY_GAME_STATE_HISTORY]
        except KeyError:
            history = []
        else:
            history = [HistoryElement.from_json(history_data) for history_data in history_datas]
        
        self.history = history
        return self
    
    
    def to_json(self):
        data = {}
        source = self.source
        
        data[JSON_KEY_GAME_STATE_SOURCE] = (source.chapter_index, source.difficulty_index, source.index, self.best)
        
        if not self.has_skill:
            data[JSON_KEY_GAME_STATE_SOURCE] = False
        
        if not self.next_skill:
            data[JSON_KEY_GAME_STATE_NEXT_SKILL] = False
        
        history = self.history
        if history:
            data[JSON_KEY_GAME_STATE_HISTORY] = [history_element.to_json() for history_element in history]
            data[JSON_KEY_GAME_STATE_POSITION] = self.position
            data[JSON_KEY_GAME_STATE_MAP] = self.map.copy()
        
        return data
    
    
    def done(self):
        targets = self.source.targets
        for tile in self.map:
            if tile == BIT_MASK_BOX_TARGET:
                targets -= 1
                if targets == 0:
                    if self.best == -1 or self.best > len(self.history):
                        self.best = len(self.history)
                    
                    return True
        
        return False
    
    def move_north(self):
        return self.move(-self.source.x_size, BIT_MASK_CHAR_N)
    
    def move_east(self):
        return self.move(1, BIT_MASK_CHAR_E)
    
    def move_south(self):
        return self.move(self.source.x_size, BIT_MASK_CHAR_S)
    
    def move_west(self):
        return self.move(-1, BIT_MASK_CHAR_W)
    
    def get_move_directories(self):
        if self.next_skill:
            return self.chapter_index.skill_get_move_directories(self)
        else:
            return self.get_own_move_directories()
    
    def get_own_move_directories(self):
        
        x_size = self.source.x_size
        position = self.position
        map_ = self.map
        
        move_directories = MoveDirectories()
        
        for step, descriptor in zip((-x_size, 1, x_size, -1), SKILL_DIRECTORY_DESCRIPTORS):
            target_tile = map_[position+step]
            
            if target_tile&BIT_MASK_UNPUSHABLE:
                can_go_to_directory = False
            elif target_tile&BIT_MASK_PASSABLE:
                can_go_to_directory = True
            else:
                after_tile = map_[position+(step<<1)]
                if target_tile&BIT_MASK_PUSHABLE and after_tile&(BIT_MASK_PASSABLE|BIT_MASK_HOLE_U):
                    can_go_to_directory = True
                else:
                    can_go_to_directory = False
            
            descriptor(move_directories, can_go_to_directory)
        
        return move_directories
    
    def move(self, step, align):
        if self.next_skill:
            result = self.source.use_skill(self, step, align)
            if result:
                self.next_skill = False
            return result
        
        map_ = self.map
        position = self.position
        
        actual_tile = map_[position]
        target_tile = map_[position+step]
        
        if target_tile&BIT_MASK_UNPUSHABLE:
            return False
        
        if target_tile&BIT_MASK_PASSABLE:
            self.history.append(HistoryElement(position, False, (
                (position, actual_tile), (position+step, target_tile))))
            
            map_[position] = actual_tile&BIT_MASK_PASSABLE
            self.position = position = position+step
            map_[position] = target_tile|align
            
            return True

        after_tile = map_[position+(step<<1)]

        if target_tile&BIT_MASK_PUSHABLE and after_tile&(BIT_MASK_PASSABLE|BIT_MASK_HOLE_U):
            self.history.append(HistoryElement(position, False, (
                (position, actual_tile), (position+step, target_tile), (position+(step<<1), after_tile))))
            
            map_[position] = actual_tile&BIT_MASK_PASSABLE
            self.position = position = position+step
            map_[position] = (target_tile>>3)|align
            if after_tile&BIT_MASK_PASSABLE:
                map_[position+step] = after_tile<<3
            else:
                map_[position+step] = BIT_MASK_HOLE_P
            return True
        
        return False
    
    def can_activate_skill(self):
        if not self.has_skill:
            return False
        
        if self.chapter_index.can_activate_skill(self):
            return True
        
        return False
    
    
    def activate_skill(self):
        if not self.has_skill:
            return False
        
        if self.next_skill:
            self.next_skill = False
            return True
        
        if self.chapter_index.activate_skill(self):
            self.next_skill = True
            return True
        
        return False
    
    def get_button_skill(self):
        chapter = self.chapter_index
        if self.next_skill:
            button = chapter.button_skill_activated
        elif self.has_skill:
            button = chapter.button_skill_used
        elif self.chapter_index.can_activate_skill(self):
            button = chapter.button_skill_enabled
        else:
            button = chapter.button_skill_disabled
        
        return button
    
    def render_description(self):
        style = self.chapter_index.style
        result = []
        map_ = self.map
        limit = len(map_)
        step = self.source.x_size
        
        if limit <= 75:
            start = 0
            shift = 0
        else:
            step_count = limit//step
            if step_count < step:
                if (step_count * (step-2)) <= 75:
                    start = 1
                    step -= 2
                    shift = 2
                else:
                    start = step+1
                    limit -= step
                    step -= 2
                    shift = 2
            else:
                if ((step_count-2) * step) <= 75:
                    start = step
                    limit -= step
                    shift = 0
                else:
                    start = step+1
                    limit -= step
                    step -= 2
                    shift = 2
        
        while start < limit:
            end = start+step
            result.append(''.join([style[element] for element in map_[start:end]]))
            start = end+shift
        
        return '\n'.join(result)
    
    def render(self):
        source = self.source
        difficulty_name = DIFFICULTY_NAMES.get(source.difficulty_index, '???')
        title = f'{source.chapter_index+1} {difficulty_name} {source.index} {self.chapter_index.emoji.as_emoji}'
        description = self.render_description()
        color = DIFFICULTY_COLORS.get(source.difficulty_index, DS_COLOR)
        
        embed = Embed(title, description, color=color)
        
        button_skill = self.get_button_skill()
        
        directories = self.get_move_directories()
        
        if directories.west:
            button_west = BUTTON_WEST_ENABLED
        else:
            button_west = BUTTON_WEST_DISABLED
        
        if directories.north:
            button_north = BUTTON_NORTH_ENABLED
        else:
            button_north = BUTTON_NORTH_DISABLED
        
        if directories.south:
            button_south = BUTTON_SOUTH_ENABLED
        else:
            button_south = BUTTON_SOUTH_DISABLED
        
        if directories.east:
            button_east = BUTTON_EAST_ENABLED
        else:
            button_east = BUTTON_EAST_DISABLED
        
        if self.can_back_or_reset():
            button_back = BUTTON_BACK_ENABLED
            button_reset = BUTTON_RESET_ENABLED
        else:
            button_back = BUTTON_BACK_DISABLED
            button_reset = BUTTON_RESET_DISABLED
        
        components = (
            Row(BUTTON_EMPTY , button_north , BUTTON_EMPTY , button_back   ,),
            Row(button_west  , button_skill , button_east  , button_reset  ,),
            Row(BUTTON_EMPTY , button_south , BUTTON_EMPTY , BUTTON_CANCEL ,),
        )
        
        return embed, components
    
    def can_back_or_reset(self):
        if self.next_skill:
            return True
        
        if self.history:
            return True
        
        return False
    
    def back(self):
        if self.next_skill:
            self.next_skill = False
            return True
        
        history = self.history
        if not history:
            return False
        
        element = history.pop(-1)
        map_ = self.map
        self.position = element.position
        
        for position, value in element.changes:
            map_[position] = value
        
        if element.was_skill:
            self.has_skill = True
        
        return True
    
    def reset(self):
        history = self.history
        if not history:
            return False
        
        history.clear()
        
        self.position = self.source.start
        self.map = self.source.map.copy()
        self.has_skill = True
        
        return True


SLASH_CLIENT : Client

DUNGEON_SWEEPER = SLASH_CLIENT.interactions(None,
    name = 'ds',
    description = 'Touhou themed puzzle game.',
    is_global = True,
)


@DUNGEON_SWEEPER.interactions
async def rules(client, event):
    """Shows the rules of DS!"""
    if not event.channel.cached_permissions_for(client).can_use_external_emojis:
        abort('I have no permissions at this channel to render this message.')
    
    return RULES_HELP


@DUNGEON_SWEEPER.interactions(is_default=True)
async def play(client, event):
    """Starts the game"""
    permissions = event.channel.cached_permissions_for(client)
    if not (permissions.can_send_messages and permissions.can_add_reactions and permissions.can_use_external_emojis \
            and permissions.can_manage_messages):
        abort('I have not all permissions to start a game at this channel.')
        return
    
    game = DS_GAMES.get(event.user.id, None)
    if game is None:
        yield DungeonSweeperRunner(client, event)
    else:
        yield game.renew(event)


def can_play_selected_chapter(user_state):
    selected_chapter_identifier = user_state.selected_chapter
    if selected_chapter_identifier == 0:
        can_play_chapter = True
    else:
        user_chapters = user_state.results
        if selected_chapter_identifier in user_chapters:
            can_play_chapter = True
        else:
            before_chapter_identifier = selected_chapter_identifier-1
            try:
                before_chapter = before_chapter_identifier[before_chapter_identifier]
            except KeyError:
                can_play_chapter = False
            else:
                try:
                    difficulty = before_chapter[CHAPTER_UNLOCK_DIFFICULTY]
                except KeyError:
                    can_play_chapter = False
                else:
                    if CHAPTER_UNLOCK_STAGE in difficulty:
                        can_play_chapter = True
                    else:
                        can_play_chapter = False
    
    return can_play_chapter


def get_selectable_stages(user_state):
    stages = []
    user_chapters = user_state.results.get(user_state.selected_chapter, None)
    
    for difficulty_index, difficulty in enumerate(CHAPTERS[user_state.selected_chapter].difficulties):
        if user_chapters is None:
            user_difficulty = None
        else:
            user_difficulty = user_state.results.get(difficulty_index, None)
        
        if user_difficulty is None:
            stages.append((difficulty[0], -1))
            break
        
        for stage_index, stage in enumerate(difficulty):
            user_best = user_difficulty.get(stage_index, None)
            if user_best is None:
                stages.append((stage, -1))
                break
            
            stages.append((stage, user_best))
            continue
        else:
            continue
        
        break
    
    selected_stage = user_state.selected_stage
    selected_difficulty = user_state.selected_difficulty
    
    for index, (stage, best) in enumerate(stages):
        if stage.difficulty_index == selected_difficulty and stage.index == selected_stage:
            selected_index = index
            break
    else:
        selected_index = 0
    
    stages_selected = []
    for (stage, best) in stages[max(selected_index-3, 0):selected_index+4]:
        if stage.difficulty_index == selected_difficulty and stage.index == selected_stage:
            is_selected = True
        else:
            is_selected = False
        
        stages_selected.append((stage, best, is_selected))
    
    return stages_selected


def render_menu(user_state):
    chapter = CHAPTERS[user_state.selected_chapter]
    embed = Embed(f'Chapter {chapter.identifier+1}').add_thumbnail(chapter.emoji.url)
    
    if can_play_selected_chapter(user_state):
        selected_stages = get_selectable_stages(user_state)
        for stage, best, is_selected in selected_stages:
            difficulty_name = DIFFICULTY_NAMES.get(stage.difficulty_index, '???')
            field_name = f'{difficulty_name} level {stage.level+1}'
            if best == -1:
                field_value = 'No results recorded yet!'
            else:
                rating = get_rating_for(stage, best)
                field_value = f'rating {rating}; steps : {best}'
            
            if is_selected:
                field_name = f'**{field_name}**'
                field_value = f'**{field_value}**'
                color = DIFFICULTY_COLORS.get(stage.difficulty_index, DS_COLOR)
            
            embed.add_field(field_name, field_value)
        
        embed.color = color
        
        if chapter.identifier+1 in CHAPTERS:
            button_chapter_next = BUTTON_RIGHT_ENABLED
        else:
            button_chapter_next = BUTTON_RIGHT_DISABLED
        
        if chapter.identifier == 0:
            button_chapter_before = BUTTON_LEFT_DISABLED
        else:
            button_chapter_before = BUTTON_LEFT_ENABLED
        
        if selected_stages[0][2]:
            button_stage_before = BUTTON_DOWN_DISABLED
            button_stage_before2 = BUTTON_DOWN2_DISABLED
        else:
            button_stage_before = BUTTON_DOWN_ENABLED
            button_stage_before2 = BUTTON_DOWN2_ENABLED
        
        if selected_stages[-1][2]:
            button_stage_after = BUTTON_UP_DISABLED
            button_stage_after2 = BUTTON_UP2_DISABLED
        else:
            button_stage_after = BUTTON_UP_ENABLED
            button_stage_after2 = BUTTON_UP2_ENABLED
        
    else:
        chapter = CHAPTERS[user_state.selected_chapter]
        embed.color = COLOR_TUTORIAL
        embed.description = (
            f'**You must finish chapter {user_state.selected_chapter} {CHAPTER_UNLOCK_DIFFICULTY_NAME} '
            f'{CHAPTER_UNLOCK_STAGE} first.**',
            )
        
        if chapter.identifier+1 in CHAPTERS:
            button_chapter_next = BUTTON_RIGHT_ENABLED
        else:
            button_chapter_next = BUTTON_RIGHT_DISABLED
        
        button_chapter_before = BUTTON_LEFT_DISABLED
        
        button_stage_before = BUTTON_DOWN_DISABLED
        button_stage_before2 = BUTTON_DOWN2_DISABLED
        
        button_stage_after = BUTTON_UP_DISABLED
        button_stage_after2 = BUTTON_UP2_DISABLED

    components = (
        Row(BUTTON_EMPTY          , button_stage_after     , button_stage_after2   , BUTTON_EMPTY        ,),
        Row(button_chapter_before , BUTTON_SELECT_DISABLED , BUTTON_CANCEL         , button_chapter_next ,),
        Row(BUTTON_EMPTY          , button_stage_before    , button_stage_before2  , BUTTON_EMPTY        ,),
    )
    
    return embed, components



class DungeonSweeperRunner:
    __slots__ = ('client', 'user', 'message', 'user_state')
    
    async def __new__(cls, client, event):
        if not event.channel.cached_permissions_for(client).can_manage_messages:
            await client.interaction_response_message_create(event, 'I need manage messages permission in the channel '
                'to execute this command.', show_for_invoking_user_only=True)
            return
        
        user_id = event.user.id
        try:
            existing_game = DS_GAMES[user_id]
        except KeyError:
            pass
        else:
            if (existing_game is None):
                await client.interaction_response_message_create(event, 'A game is already starting somewhere else.',
                    show_for_invoking_user_only=True)
            else:
                await existing_game.renew(event)
            return
        
        DS_GAMES[user_id] = None
        try:
            async with DB_ENGINE.connect() as connector:
                response = await connector.execute(
                    select([ds_v2_model.data]). \
                    where(ds_v2_model.user_id==user_id)
                )
                
                results = await response.read()
                if results:
                    raw_data = results[0][0]
                    
                    user_state = UserState.from_raw_data(raw_data)
                else:
                    user_state = UserState()
            
            game_state = user_state.game_state
            if game_state is None:
                embed, components = render_menu(user_state)
            else:
                embed, components = game_state.render(user_state)
            
            user = event.user
            embed.add_author(user.avatar_url_as('png', 32), user.full_name)
            
            await client.interaction_response_message_create(event, embed=embed, components=components)
            message = await event.wait_for_response_message(timeout=10.0)
        except:
            del DS_GAMES[user_id]
            raise
        
        self = object.__new__(cls)
        self.client = client
        self.user = event.user
        self.message = message
        self.user_state = user_state
        DS_GAMES[user_id] = self
        client.slasher.add_component_interaction_waiter(message, self)
        return self
    
    async def __call__(self, event):
    
