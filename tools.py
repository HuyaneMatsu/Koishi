import re
from weakref import WeakKeyDictionary
from random import random

from hata import CancelledError, sleep, Task, DiscordException
from hata.events import CommandProcesser
from hata.parsers import EventHandlerBase

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup=None

def choose(list_):
    return list_[int((random()*len(list_)))]

def choose_notsame(list_,last):
    index=int(random()*len(list_))
    value=list_[index]
    if value==last:
        index=index+1
        if index==len(list_):
            index=0
        value=list_[index]

    return value

def pop_one(list_):
    return list_.pop(int((random()*len(list_))))

def mark_as_async(func):
    func.__async_call__=True
    return func

def smart_join(list_,limit=2000,sep='\n'):
    result=[]
    seplen=len(sep)
    limit-=(3+seplen)
    for value in list_:
        limit-=(len(value)+seplen)
        if limit<0:
            result.append('...')
            break
        result.append(value)
    return sep.join(result)

class MessageDeleteWaitfor(EventHandlerBase):
    __slots__=('waitfors',)
    __event_name__='message_delete'
    def __init__(self):
        self.waitfors=WeakKeyDictionary()

    async def __call__(self,client,message):
        try:
            event=self.waitfors[message.channel]
        except KeyError:
            return
        await event(client,message)

    append=CommandProcesser.append
    remove=CommandProcesser.remove
    
class CooldownHandler:
    __slots__=('cache',)
    def __init__(self):
        self.cache={}

    async def __call__(self,client,message,command,time_left):
        user_id=message.author.id
        try:
            notification,waiter=self.cache[user_id]
        except KeyError:
            pass
        else:
            if notification.channel is message.channel:
                try:
                    await client.message_edit(notification,f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!')
                except DiscordException:
                    pass
                return

            waiter.cancel()

        try:
            notification = await client.message_create(message.channel,f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!')
        except DiscordException:
            return

        waiter=Task(self.waiter(client,user_id,notification),client.loop)
        self.cache[user_id]=(notification,waiter)

    async def waiter(self,client,user_id,notification):
        try:
            await sleep(30.,client.loop)
        except CancelledError:
            pass
        del self.cache[user_id]
        try:
            await client.message_delete(notification)
        except DiscordException:
            pass

del CommandProcesser
del re
