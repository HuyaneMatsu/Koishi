import re
from weakref import WeakKeyDictionary
from hata.events import CommandProcesser
from hata.embed import Embed
from hata.futures import CancelledError,sleep,Task
from hata.dereaddons_local import inherit
from hata import others
from hata.exceptions import DiscordException
from random import random

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup=None

def choose(list_):
    return list_[(random()*list_.__len__()).__int__()]

def choose_notsame(list_,last):
    index=(random()*list_.__len__()).__int__()
    value=list_[index]
    if value==last:
        index=index+1
        if index==list_.__len__():
            index=0
        value=list_[index]

    return value

def pop_one(list_):
    return list_.pop((random()*list_.__len__()).__int__())

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

@inherit(CommandProcesser)
class MessageDeleteWaitfor(object):
    __slots__=['waitfors']
    __event_name__='message_delete'
    def __init__(self):
        self.waitfors=WeakKeyDictionary()

    async def __call__(self,client,message):
        try:
            event=self.waitfors[message.channel]
        except KeyError:
            return
        await event(message)

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

class commit_extractor(object):
    _GIT_RP=re.compile('^\[`[\da-f]*`\]\((https://github.com/[^/]*/[^/]*/)commit')
    __slots__=('channel', 'client', 'color', 'role', 'webhook',)
    def __init__(self,client,channel,webhook,role=None,color=0):
        self.client=client
        self.channel=channel
        self.webhook=webhook
        self.role=role
        self.color=color

    async def __call__(self,message):
        webhook=self.webhook
        client=self.client

        if message.author!=webhook or message.author.name!='GitHub':
            return
        
        embed=message.embeds[0]

        if ':master' not in embed.title:
            return

        url=self._GIT_RP.match(embed.description).group(1)+'commit/master'
        result = await client.download_url(url)
        soup=BeautifulSoup(result,'html.parser',from_encoding='utf-8')
        
        description_container=soup.find(class_='commit-desc')
        if description_container is None:
            return
        
        title_container=soup.find(class_='commit-title')

        if webhook.partial:
            await client.webhook_update(webhook)

        guild=webhook.guild
        
        if self.role is None:
            result_content=''
            needs_unlock=False
        else:
            result_content=self.role.mention
            needs_unlock = (not self.role.mentionable) and guild.permissions_for(client).can_manage_roles

        embed_text=others.chunkify(description_container.getText('\n').splitlines())
        result_embed=Embed(
            title       = title_container.getText('\n').strip(),
            description = embed_text[0],
            color       = self.color,
            url         = url,
                )

        extra_embeds=[]
        for index in range(1,min(len(embed_text),9)):
            extra_embeds.append(
                Embed(
                    title       = '',
                    description = embed_text[index],
                    color       = self.color,
                    url         = '',
                        )
                )
            
        webhook_name = embed.author.name
        webhook_avatar_url = embed.author.proxy_icon_url

        if needs_unlock:
            try:
                await client.role_edit(self.role,mentionable=True)
                await sleep(0.8,client.loop)
                await client.webhook_send(webhook,
                    result_content,
                    result_embed,
                    name=webhook_name,
                    avatar_url=webhook_avatar_url
                        )
                for embed in extra_embeds:
                    await client.webhook_send(webhook,
                        '',
                        embed,
                        name=webhook_name,
                        avatar_url=webhook_avatar_url
                            )
                await sleep(0.8,client.loop)
            finally:
                await client.role_edit(self.role,mentionable=False)

        else:
            await client.webhook_send(webhook,
                result_content,
                result_embed,
                name=webhook_name,
                avatar_url=webhook_avatar_url
                    )
del CommandProcesser
del inherit
del re
