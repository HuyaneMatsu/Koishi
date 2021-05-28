# Work in progress
'''
import re, os

from hata import Emoji, Embed, Color, DiscordException, BUILTIN_EMOJIS, Task, WaitTillAll, ERROR_CODES, Client, \
    KOKORO, LOOP_TIME

from hata.ext.command_utils import GUI_STATE_READY, GUI_STATE_SWITCHING_PAGE, GUI_STATE_CANCELLING, \
    GUI_STATE_SWITCHING_CTX, GUI_STATE_CANCELLED
from hata.ext.commands_v2 import checks

from hata.discord.core import GC_CYCLER
from hata.ext.slash import SlashResponse, abort, Row, Button, ButtonStyle


from bot_utils.models import DB_ENGINE, DS_TABLE, ds_model
from bot_utils.shared import PATH__KOISHI


DS_COLOR = Color(0xa000c4)

DS_GAMES = {}
STAGES = []
CHARS = []
COLORS = (0xa000c4, 0x00cc03, 0xffe502, 0xe50016)

EMOJI_WEST   = BUILTIN_EMOJIS['arrow_left']
EMOJI_NORTH  = BUILTIN_EMOJIS['arrow_up']
EMOJI_SOUTH  = BUILTIN_EMOJIS['arrow_down']
EMOJI_EAST   = BUILTIN_EMOJIS['arrow_right']

EMOJI_BACK   = BUILTIN_EMOJIS['leftwards_arrow_with_hook']
EMOJI_RESET  = BUILTIN_EMOJIS['arrows_counterclockwise']
EMOJI_CANCEL = BUILTIN_EMOJIS['x']

EMOJI_UP     = BUILTIN_EMOJIS['arrow_up_small']
EMOJI_DOWN   = BUILTIN_EMOJIS['arrow_down_small']
EMOJI_UP2    = BUILTIN_EMOJIS['arrow_double_up']
EMOJI_DOWN2  = BUILTIN_EMOJIS['arrow_double_down']
EMOJI_LEFT   = BUILTIN_EMOJIS['arrow_backward']
EMOJI_RIGHT  = BUILTIN_EMOJIS['arrow_forward']
EMOJI_SELECT = BUILTIN_EMOJIS['ok']

EMOJI_NOTHING = Emoji.precreate(568838460434284574, name='0Q')

EMOJI_REIMU = Emoji.precreate(574307645347856384, name='REIMU')
EMOJI_FURANDOORU = Emoji.precreate(575387120147890210, name='FURANDOORU')
EMOJI_YUKARI = Emoji.precreate(575389643424661505, name='YUKARI')

IDENTIFIER_UP = '1'
IDENTIFIER_DOWN = '2'
IDENTIFIER_UP2 = '3'
IDENTIFIER_DOWN2 = '4'
IDENTIFIER_LEFT = '5'
IDENTIFIER_SELECT = '6'

IDENTIFIER_EMPTY = '_'
IDENTIFIER_SKILL = '0'

SLASH_CLIENT : Client

DUNGEON_SWEEPER = SLASH_CLIENT.interactions(None,
    name='ds',
    description='Touhou themed puzzle game.',
    is_global=True,
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
        yield DSRunner(event)
    else:
        yield game.renew(event)


class DSRunner():
    BUTTON_UP = Button(emoji=EMOJI_UP, custom_id=IDENTIFIER_UP, style=ButtonStyle.violet)
    BUTTON_DOWN = Button(emoji=EMOJI_DOWN, custom_id=IDENTIFIER_DOWN, style=ButtonStyle.violet)
    BUTTON_UP2 = Button(emoji=EMOJI_UP2, custom_id=IDENTIFIER_UP2, style=ButtonStyle.violet)
    BUTTON_DOWN2 = Button(emoji=EMOJI_DOWN2, custom_id=IDENTIFIER_DOWN2, style=ButtonStyle.violet)
    BUTTON_LEFT = Button(emoji=EMOJI_LEFT, custom_id=IDENTIFIER_LEFT, style=ButtonStyle.violet)
    BUTTON_RIGHT = Button(emoji=EMOJI_RIGHT, custom_id=EMOJI_RIGHT, style=ButtonStyle.violet)
    BUTTON_SELECT = Button('Lets go!', EMOJI_SELECT, custom_id=IDENTIFIER_SELECT, style=ButtonStyle.green)
    
    BUTTON_EMPTY = Button('_ _', custom_id=IDENTIFIER_EMPTY, style=ButtonStyle.gray, enabled=False)
    
    BUTTON_SPECIAL_SKILL = Button(custom_id=IDENTIFIER_SKILL, style=ButtonStyle.violet)
    
    MENU_ROW_1 = Row(BUTTON_EMPTY, BUTTON_UP, BUTTON_EMPTY)
    MENU_ROW_2 = Row(BUTTON_LEFT, BUTTON_SELECT, BUTTON_RIGHT)
    MENU_ROW_3 = Row(BUTTON_EMPTY, BUTTON_DOWN, BUTTON_EMPTY)
    
    GAME_ROW_ =
    





'''
