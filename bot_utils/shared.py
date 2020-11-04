# -*- coding: utf-8 -*-
import os
from io import StringIO
from hata import ChannelText, Guild, Role, Invite, Color, Embed, KOKORO
from hata.ext.commands import Pagination

import config

from config import KOISHI_PATH
if KOISHI_PATH is None:
    KOISHI_PATH = os.path.abspath('..')

KOISHI_PREFIX = config.KOISHI_PREFIX
SATORI_PREFIX = config.SATORI_PREFIX
FLAN_PREFIX = config.FLAN_PREFIX
MARISA_PREFIX = config.MARISA_PREFIX

DUNGEON = Guild.precreate(388267636661682178)

WELCOME_CHANNEL = ChannelText.precreate(445191707491958784)
EVERYNYAN_ROLE = Role.precreate(445189164703678464)
ANNOUNCEMNETS_ROLE = Role.precreate(538397994421190657)
WORSHIPPER_ROLE = Role.precreate(403586901803794432)
DUNGEON_PREMIUM_ROLE = Role.precreate(585556522558554113)
DUNGEON_INVITE = Invite.precreate('3cH2r5d')

DEFAULT_CATEGORY_NAME = 'Uncategorized'

SATORI_HELP_COLOR = Color.from_rgb(118, 0, 161)
KOISHI_HELP_COLOR = Color.from_html('#ffd21e')
FLAN_HELP_COLOR = Color.from_rgb(230, 69, 0)
MARISA_HELP_COLOR = Color.from_html('#e547ed')

KOISHI_GIT = 'https://github.com/HuyaneMatsu/Koishi'
HATA_GIT = 'https://github.com/HuyaneMatsu/hata'
HATA_DOCS = 'https://huyanematsu.pythonanywhere.com/docs/hata'
TORTOISE_PASTE = "https://paste.tortoisecommunity.com/"

SYNC_CHANNEL = ChannelText.precreate(568837922288173058)

async def permission_check_handler(client, message, command, check):
    permission_names = ' '.join(permission_name.replace('_', ' ') for permission_name in check.permissions)
    await client.message_create(message.channel,
        f'You must have {permission_names} permission to invoke `{command.display_name}` command.')

async def not_guild_owner_handler(client, message, command, check):
    await client.message_create(message.channel,
        f'You must be the owner of the guild to invoke `{command.display_name}` command.')

async def not_bot_owner_handler(client, message, command, check):
    await client.message_create(message.channel,
        f'You must be the owner of the bot to invoke `{command.display_name}` command.')

def category_name_rule(name):
    if name is None:
        name = DEFAULT_CATEGORY_NAME
    else:
        name = name.capitalize()
    
    return name

async def command_error(client, message, command, content, exception):
    with StringIO() as buffer:
        await KOKORO.render_exc_async(exception,[
            client.full_name,
            ' ignores an occured exception at command ',
            repr(command),
            '\n\nMessage details:\nGuild: ',
            repr(message.guild),
            '\nChannel: ',
            repr(message.channel),
            '\nAuthor: ',
            message.author.full_name,
            ' (',
            repr(message.author.id),
            ')\nContent: ',
            repr(content),
            '\n```py\n'], '```', file=buffer)
        
        buffer.seek(0)
        lines = buffer.readlines()
    
    pages = []
    
    page_length = 0
    page_contents = []
    
    index = 0
    limit = len(lines)
    
    while True:
        if index == limit:
            embed = Embed(description=''.join(page_contents))
            pages.append(embed)
            page_contents = None
            break
        
        line = lines[index]
        index = index+1
        
        line_lenth = len(line)
        # long line check, should not happen
        if line_lenth > 500:
            line = line[:500]+'...\n'
            line_lenth = 504
        
        if page_length+line_lenth > 1997:
            if index == limit:
                # If we are at the last element, we dont need to shard up,
                # because the last element is always '```'
                page_contents.append(line)
                embed = Embed(description=''.join(page_contents))
                pages.append(embed)
                page_contents = None
                break
            
            page_contents.append('```')
            embed = Embed(description=''.join(page_contents))
            pages.append(embed)
            
            page_contents.clear()
            page_contents.append('```py\n')
            page_contents.append(line)
            
            page_length = 6+line_lenth
            continue
        
        page_contents.append(line)
        page_length += line_lenth
        continue
    
    limit = len(pages)
    index = 0
    while index < limit:
        embed = pages[index]
        index += 1
        embed.add_footer(f'page {index}/{limit}')
    
    await Pagination(client, message.channel, pages)
    return False

class WrapMultyple(object):
    __slots__ = ('elements')
    def __init__(self, *elements):
        self.elements = elements
    
    def __call__(self, func=None, **kwargs):
        if func is not None:
            return self.add(func, kwargs)
        else:
            return self._wrapper(self, kwargs)
    
    def add(self, func, kwargs):
        result = None
        for element in self.elements:
            result = element(func, **kwargs)
        
        return result
    
    class _wrapper(object):
        __slots__ = ('parent', 'kwargs')
        def __init__(self, parent, kwargs):
            self.parent = parent
            self.kwargs = kwargs
        
        def __call__(self, func):
            return self.parent.add(func, self.kwargs)
