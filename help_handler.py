# -*- coding: utf-8 -*-
from hata.embed import Embed
from hata.events import Pagination
from hata.color import Color
from hata.exceptions import DiscordException
from hata.futures import sleep
from hata.permission import Permission

class _HelperE(object):
    __slots__=('name', 'coro', 'checker')

class Helper(object):
    __slots__=('default','invalid','no_perm','helps','helps_by_name')
    def __init__(self,default,invalid,no_perm):
        self.default        = default
        self.invalid        = invalid
        self.no_perm        = no_perm
        self.helps          = []
        self.helps_by_name = {}

    def add(self,name,coro,checker=None):
        if len(name)>64:
            raise ValueError('name over 64 character')

        if (checker is not None):
            if not callable(checker):
                raise TypeError(f'Checker should be callable, got {checker!r}.\nname = \'{name}\'\ncoro = {coro!r}')
            
        element=object.__new__(_HelperE)
        element.name    = name
        element.coro    = coro
        element.checker = checker

        self.helps.append(element)
        self.helps_by_name[name]=element

    def sort(self):
        self.helps.sort(key=lambda e:e.name)

    @staticmethod
    def check_is_owner(client,message):
        return client.is_owner(message.author)

    @staticmethod
    def check_is_guild_owner(client,message):
        if client.is_owner(message.author):
            return True

        guild=message.channel.guild
        if guild is None:
            return False

        return guild.owner==message.author

    class check_permission(object):
        def __init__(self,perms):
            self.perms=perms
        def __call__(self,client,message):
            if client.is_owner(message.author):
                return True

            return message.channel.permissions_for(message.author).is_superset(self.perms)

    async def __call__(self,client,message,content):
        if not (0<len(content)<64):
            await self.default(client,message,self)
            return
        
        content=content.lower()
        try:
            result=self.helps_by_name[content]
        except KeyError:
            await self.invalid(client,message,content)
            return

        checker=result.checker
        if (checker is not None) and (not checker(client,message)):
            await self.no_perm(client,message)
            return

        await result.coro(client,message)

KOISHI_HELP_COLOR=Color.from_html('#ffd21e')

async def _koishi_help_default(client,message,helper):
    pages=[]
    part=[]
    index=0
    for element in helper.helps:
        checker=element.checker
        if (checker is not None) and (not checker(client,message)):
            continue

        if index==16:
            pages.append('\n'.join(part))
            part.clear()
            index=0
        part.append(f'**>>** {element.name}')
        index+=1

    pages.append('\n'.join(part))

    del part

    prefix=client.events.message_create.prefix(message)
    result=[]

    limit=len(pages)
    index=0
    while index<limit:
        embed=Embed('Commands:',color=KOISHI_HELP_COLOR,description=pages[index])
        index+=1
        embed.add_field(f'Use `{prefix}help <command>` for more information.',f'page {index}/{limit}')
        result.append(embed)

    del pages

    await Pagination(client,message.channel,result)

async def _koishi_help_invalid(client,message,content):
    prefix=client.events.message_create.prefix(message)
    embed=Embed(f'Invalid command: {content}',(
        f'Please try using `{prefix}help` to list the available commands '
        'for you\n'
        'Take care!'
        ),color=KOISHI_HELP_COLOR)
    message = await client.message_create(message.channel,embed=embed)
    await sleep(30.,client.loop)
    await client.message_delete(message)

async def _koishi_help_no_perm(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('Permission denied',(
        f'Please try using `{prefix}help` to list the available commands '
        'for you\n'
        'Love you!'
        ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)
    await sleep(30.,client.loop)
    await client.message_delete(message)

KOISHI_HELPER=Helper(_koishi_help_default,_koishi_help_invalid,_koishi_help_no_perm)
KOISHI_HELPER.add('help',_koishi_help_default)

async def invalid_command(client,message,command,content):
    prefix=client.events.message_create.prefix(message)
    embed=Embed(
        f'Invalid command `{command}`',
        f'try using: `{prefix}help`',
        color=KOISHI_HELP_COLOR,
            )
    
    message = await client.message_create(message.channel,embed=embed)
    await sleep(30.,client.loop)
    await client.message_delete(message)

