# -*- coding: utf-8 -*-
import re
from random import random

from hata import CancelledError, sleep, Task, DiscordException, methodize, ERROR_CODES, BUILTIN_EMOJIS, \
    EventWaitforBase, KOKORO, ERROR_CODES
from hata.ext.commands import CommandProcesser, Timeouter, GUI_STATE_READY, GUI_STATE_SWITCHING_PAGE, \
    GUI_STATE_CANCELLING, GUI_STATE_CANCELLED, GUI_STATE_SWITCHING_CTX

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
    return list_[int((random()*len(list_)))]

def choose_notsame(list_,last):
    index = int(random()*len(list_))
    value = list_[index]
    if value == last:
        index +=1
        if index == len(list_):
            index = 0
        value = list_[index]

    return value

def pop_one(list_):
    return list_.pop(int((random()*len(list_))))

def smart_join(list_,limit=2000,sep='\n'):
    result = []
    seplen = len(sep)
    limit -= (3+seplen)
    for value in list_:
        limit -= (len(value)+seplen)
        if limit < 0:
            result.append('...')
            break
        result.append(value)
    return sep.join(result)

class MessageDeleteWaitfor(EventWaitforBase):
    __event_name__ = 'message_delete'

class MessageEditWaitfor(EventWaitforBase):
    __event_name__ = 'message_edit'

class GuildDeleteWaitfor(EventWaitforBase):
    __event_name__ = 'guild_delete'

class RoleDeleteWaitfor(EventWaitforBase):
    __event_name__ = 'role_delete'

class ChannelDeleteWaitfor(EventWaitforBase):
    __event_name__ = 'channel_delete'

class EmojiDeleteWaitfor(EventWaitforBase):
    __event_name__ = 'emoji_delete'

class RoleEditWaitfor(EventWaitforBase):
    __event_name__ = 'role_edit'

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
                    await client.message_edit(notification,
                        f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!')
                except BaseException as err:
                    if isinstance(err, ConnectionError):
                        return
                    
                    if isinstance(err, DiscordException):
                        if err.code in (
                                ERROR_CODES.unknown_message, # message deleted
                                ERROR_CODES.unknown_channel, # channel deleted
                                ERROR_CODES.invalid_access, # client removed
                                    ):
                            return
                    
                    await client.events.error(client, f'{self!r}.__call__', err)
                
                return
            
            waiter.cancel()
        
        try:
            notification = await client.message_create(message.channel,
                f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!')
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                        ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.__call__', err)
        
        waiter = Task(self.waiter(client, user_id, notification), KOKORO)
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
                        ERROR_CODES.invalid_access, # client removed
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.__call__', err)


class PAGINATION_5PN(object):
    LEFT2 = BUILTIN_EMOJIS['rewind']
    LEFT  = BUILTIN_EMOJIS['arrow_backward']
    RIGHT = BUILTIN_EMOJIS['arrow_forward']
    RIGHT2 = BUILTIN_EMOJIS['fast_forward']
    RESET = BUILTIN_EMOJIS['arrows_counterclockwise']
    CANCEL = BUILTIN_EMOJIS['x']
    EMOJIS = (LEFT2, LEFT, RIGHT, RIGHT2, RESET, CANCEL)
    
    __slots__ = ('canceller', 'channel', 'client', 'message', 'page', 'pages', 'task_flag', 'timeouter')
    
    async def __new__(cls, client, channel, pages):
        self = object.__new__(cls)
        self.client = client
        self.channel = channel
        self.pages = pages
        self.page = 0
        self.canceller = cls._canceller
        self.task_flag = GUI_STATE_READY
        self.timeouter = None
        
        try:
            message = await client.message_create(self.channel,embed=self.pages[0])
        except BaseException as err:
            self.message = None
            
            if isinstance(err, ConnectionError):
                return None
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                        ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                            ):
                    return
            
            raise
        
        self.message = message
        
        if not channel.cached_permissions_for(client).can_add_reactions:
            return self
        
        try:
            if len(self.pages) > 1:
                for emoji in self.EMOJIS:
                    await client.reaction_add(message, emoji)
            else:
                await client.reaction_add(message, self.CANCEL)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return self
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ):
                    return self
            
            raise
            
            
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)
        self.timeouter = Timeouter(self, timeout=300.)
        return self
    
    async def __call__(self, client, event):
        if event.user.is_bot or (event.emoji not in self.EMOJIS):
            return
        
        if (event.delete_reaction_with(client) == event.DELETE_REACTION_NOT_ADDED):
            return
        
        emoji = event.emoji
        task_flag = self.task_flag
        if task_flag != GUI_STATE_READY:
            if task_flag == GUI_STATE_SWITCHING_PAGE:
                if emoji is self.CANCEL:
                    self.task_flag = GUI_STATE_CANCELLING
                return
            
            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        while True:
            if emoji is self.LEFT:
                page = self.page-1
                break
                
            if emoji is self.RIGHT:
                page = self.page+1
                break
                
            if emoji is self.RESET:
                page = 0
                break
                
            if emoji is self.CANCEL:
                self.task_flag = GUI_STATE_CANCELLED
                try:
                    await client.message_delete(self.message)
                except BaseException as err:
                    self.cancel()
                    
                    if isinstance(err,ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err,DiscordException):
                        if err.code in (
                                ERROR_CODES.invalid_access, # client removed
                                ERROR_CODES.unknown_channel, # message's channel deleted
                                    ):
                            return
                    
                    await client.events.error(client,f'{self!r}.__call__',err)
                    return
                
                else:
                    self.cancel()
                    return
            
            if emoji is self.LEFT2:
                page = self.page-10
                break
            
            if emoji is self.RIGHT2:
                page = self.page+10
                break
            
            return
        
        if page < 0:
            page = 0
        elif page >= len(self.pages):
            page = len(self.pages)-1
        
        if self.page == page:
            return
        
        self.page = page
        self.task_flag=GUI_STATE_SWITCHING_PAGE
        try:
            await client.message_edit(self.message, embed=self.pages[page])
        except BaseException as err:
            self.task_flag = GUI_STATE_CANCELLED
            self.cancel()
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.unknown_message, # message already deleted
                            ):
                    return
            
            # We definitedly do not want to silence `ERROR_CODES.invalid_form_body`
            await client.events.error(client, f'{self!r}.__call__',err)
            return
        
        if self.task_flag == GUI_STATE_CANCELLING:
            self.task_flag = GUI_STATE_CANCELLED
            try:
                await client.message_delete(self.message)
            except BaseException as err:
                
                if isinstance(err,ConnectionError):
                    # no internet
                    return
                
                if isinstance(err,DiscordException):
                    if err.code == ERROR_CODES.invalid_access: # client removed
                        return
                
                await client.events.error(client,f'{self!r}.__call__',err)
                return
            
            return
        
        self.task_flag = GUI_STATE_READY
        
        self.timeouter.set_timeout(150.0)
        
    @staticmethod
    async def _canceller(self,exception,):
        client = self.client
        message = self.message
        
        client.events.reaction_add.remove(message, self)
        client.events.reaction_delete.remove(message, self)

        if self.task_flag == GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return
        
        self.task_flag = GUI_STATE_CANCELLED
        
        if exception is None:
            return
        
        if isinstance(exception, TimeoutError):
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(message)
                except BaseException as err:
                    
                    if isinstance(err, ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err, DiscordException):
                        if err.code in (
                                ERROR_CODES.unknown_channel, # message's channel deleted
                                ERROR_CODES.invalid_access, # client removed
                                ERROR_CODES.unknown_message, # message deleted
                                ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                                    ):
                            return
                    
                    await client.events.error(client,f'{self!r}._canceller', err)
                    return
            return
        
        timeouter = self.timeouter
        if (timeouter is not None):
            timeouter.cancel()
        #we do nothing
    
    def cancel(self,exception=None):
        canceller = self.canceller
        if canceller is None:
            return
        
        self.canceller = None
        
        timeouter = self.timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        return Task(canceller(self,exception), KOKORO)

del CommandProcesser
del re
