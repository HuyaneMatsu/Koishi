from random import random

from scarletio import CancelledError, sleep, Task, methodize
from hata import DiscordException, BUILTIN_EMOJIS, EventWaitforBase, KOKORO, ERROR_CODES

from hata.ext.slash import Button, Row
from hata.ext.slash.menus.menu import Menu
from hata.ext.slash.menus.helpers import EMOJI_LEFT, EMOJI_RIGHT, EMOJI_CANCEL, get_auto_check, CUSTOM_ID_CANCEL, \
    top_level_check, top_level_get_timeout


try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

from PIL import Image as PIL
from PIL.ImageDraw import ImageDraw
from PIL.ImageFont import truetype

PIL.Image.draw = methodize(ImageDraw)
PIL.font = truetype
del ImageDraw, truetype, methodize

def choose(list_):
    return list_[int((random() * len(list_)))]

def choose_not_same(list_,last):
    index = int(random() * len(list_))
    value = list_[index]
    if value == last:
        index +=1
        if index == len(list_):
            index = 0
        value = list_[index]

    return value

def pop_one(list_):
    return list_.pop(int((random() * len(list_))))

def smart_join(list_, limit=2000, sep='\n'):
    result = []
    separator_length = len(sep)
    limit -= (3 + separator_length)
    for value in list_:
        limit -= (len(value) + separator_length)
        if limit < 0:
            result.append('...')
            break
        result.append(value)
    return sep.join(result)

class MessageDeleteWaitfor(EventWaitforBase):
    __event_name__ = 'message_delete'

class MessageUpdateWaitfor(EventWaitforBase):
    __event_name__ = 'message_update'

class GuildDeleteWaitfor(EventWaitforBase):
    __event_name__ = 'guild_delete'

class RoleDeleteWaitfor(EventWaitforBase):
    __event_name__ = 'role_delete'

class ChannelDeleteWaitfor(EventWaitforBase):
    __event_name__ = 'channel_delete'

class ChannelCreateWaitfor(EventWaitforBase):
    __event_name__ = 'channel_create'

class ChannelUpdateWaitfor(EventWaitforBase):
    __event_name__ = 'channel_update'

class EmojiDeleteWaitfor(EventWaitforBase):
    __event_name__ = 'emoji_delete'

class RoleUpdateWaitfor(EventWaitforBase):
    __event_name__ = 'role_update'

class CooldownHandler:
    __slots__ = ('cache',)
    
    def __init__(self):
        self.cache = {}
    
    async def __call__(self, client, message, command, time_left):
        user_id = message.author.id
        try:
            notification,waiter = self.cache[user_id]
        except KeyError:
            pass
        else:
            if notification.channel is message.channel:
                try:
                    await client.message_update(
                        notification,
                        f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!',
                    )
                except BaseException as err:
                    if isinstance(err, ConnectionError):
                        return
                    
                    if isinstance(err, DiscordException):
                        if err.code in (
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.missing_access, # client removed
                        ):
                            return
                    
                    await client.events.error(client, f'{self!r}.__call__', err)
                
                return
            
            waiter.cancel()
        
        try:
            notification = await client.message_create(
                message.channel,
                f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!',
            )
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.unknown_channel, # message's channel deleted
                    ERROR_CODES.missing_access, # client removed
                    ERROR_CODES.missing_permissions, # permissions changed meanwhile
                    ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                ):
                    return
            
            await client.events.error(client, f'{self!r}.__call__', err)
        
        waiter = Task(KOKORO, self.waiter(client, user_id, notification))
        self.cache[user_id] = (notification, waiter)
    
    async def waiter(self, client, user_id, notification):
        try:
            await sleep(30., KOKORO)
        except CancelledError:
            pass
        
        del self.cache[user_id]
        
        try:
            await client.message_delete(notification)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                    ERROR_CODES.unknown_channel, # message's channel deleted
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.missing_access, # client removed
                ):
                    return
            
            await client.events.error(client, f'{self!r}.__call__', err)

EMOJI_LEFT_2_10 = BUILTIN_EMOJIS['rewind']
EMOJI_RIGHT_2_10 = BUILTIN_EMOJIS['fast_forward']
EMOJI_RESET = BUILTIN_EMOJIS['arrows_counterclockwise']

class Pagination10step(Menu):
    BUTTON_LEFT_2 = Button(emoji = EMOJI_LEFT_2_10)
    BUTTON_LEFT = Button(emoji = EMOJI_LEFT)
    BUTTON_RIGHT = Button(emoji = EMOJI_RIGHT)
    BUTTON_RIGHT_2 = Button(emoji = EMOJI_RIGHT_2_10)
    BUTTON_RESET = Button(emoji = EMOJI_RESET)
    BUTTON_CANCEL = Button(emoji = EMOJI_CANCEL, custom_id = CUSTOM_ID_CANCEL)
    
    BUTTON_ROW_1 = Row(BUTTON_LEFT_2, BUTTON_LEFT, BUTTON_RIGHT, BUTTON_RIGHT_2, BUTTON_RESET,)
    BUTTON_ROW_2 = Row(BUTTON_CANCEL)
    
    __slots__ = ('page_index', 'pages', 'timeout', 'user_check')
    
    def __init__(self, client, event, pages, *, check = ..., timeout = 300.0):
        if check is ...:
            check = get_auto_check(event)
        
        self.pages = pages
        self.page_index = 0
        self.timeout = timeout
        self.user_check = check
    
    
    check = top_level_check
    get_timeout = top_level_get_timeout
    
    async def initial_invoke(self):
        self.components = [self.BUTTON_ROW_1, self.BUTTON_ROW_2]
        self.allowed_mentions = None
        self.BUTTON_LEFT_2.enabled = False
        self.BUTTON_LEFT.enabled = False
        self.BUTTON_RESET.enabled = False
        
        pages = self.pages
        self.content = pages[0]
        if len(pages) == 1:
            self.BUTTON_RIGHT_2.enabled = False
            self.BUTTON_RIGHT.enabled = False
    
    
    async def invoke(self, event):
        interaction = event.interaction
        if interaction == self.BUTTON_CANCEL:
            self.cancel(CancelledError())
            return False
        
        pages_index_limit = len(self.pages) - 1
        
        if interaction == self.BUTTON_LEFT:
            page_index = self.page_index - 1
        elif interaction == self.BUTTON_RIGHT:
            page_index = self.page_index + 1
        elif interaction == self.BUTTON_LEFT_2:
            page_index = self.page_index - 10
        elif interaction == self.BUTTON_RIGHT_2:
            page_index = self.page_index + 10
        elif interaction == self.BUTTON_RESET:
            page_index = 0
        else:
             return False
        
        if page_index < 0:
            page_index = 0
        elif page_index > pages_index_limit:
            page_index = pages_index_limit
        
        if self.page_index == page_index:
            return False
        
        if page_index == 0:
            self.BUTTON_LEFT_2.enabled = False
            self.BUTTON_LEFT.enabled = False
            self.BUTTON_RESET.enabled = False
        else:
            self.BUTTON_LEFT_2.enabled = True
            self.BUTTON_LEFT.enabled = True
            self.BUTTON_RESET.enabled = True
        
        if page_index == pages_index_limit:
            self.BUTTON_RIGHT_2.enabled = False
            self.BUTTON_RIGHT.enabled = False
        else:
            self.BUTTON_RIGHT_2.enabled = True
            self.BUTTON_RIGHT.enabled = True
        
        self.page_index = page_index
        self.content = self.pages[page_index]
        return True


class Cell:
    __slots__ = ('value', )
    def __init__(self, value = None):
        self.value = value
