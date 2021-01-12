# -*- coding: utf-8 -*-
import os
from io import StringIO
from hata import ChannelText, Guild, Role, Invite, Color, Embed, KOKORO, ChannelCategory
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
ANNOUNCEMENTS_ROLE = Role.precreate(538397994421190657)
WORSHIPPER_ROLE = Role.precreate(403586901803794432)
DUNGEON_PREMIUM_ROLE = Role.precreate(585556522558554113)
DUNGEON_INVITE = Invite.precreate('3cH2r5d')
BOT_CHANNEL_CATEGORY = ChannelCategory.precreate(445191611727478795)
STAFF_ROLE = Role.precreate(726171592509358093)
TESTER_ROLE = Role.precreate(648138238250319876)

DEFAULT_CATEGORY_NAME = 'Uncategorized'

SATORI_HELP_COLOR = Color.from_rgb(118, 0, 161)
KOISHI_HELP_COLOR = Color.from_html('#ffd21e')
FLAN_HELP_COLOR = Color.from_rgb(230, 69, 0)
MARISA_HELP_COLOR = Color.from_html('#e547ed')

KOISHI_GIT = 'https://github.com/HuyaneMatsu/Koishi'
HATA_GIT = 'https://github.com/HuyaneMatsu/hata'
HATA_DOCS = 'https://huyanematsu.pythonanywhere.com/docs/hata'
PASTE = 'https://hastebin.com/'

SYNC_CHANNEL = ChannelText.precreate(568837922288173058)

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
            ' ignores an occurred exception at command ',
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
        
        line_length = len(line)
        # long line check, should not happen
        if line_length > 500:
            line = line[:500]+'...\n'
            line_length = 504
        
        if page_length+line_length > 1997:
            if index == limit:
                # If we are at the last element, we don\'t need to shard up,
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
            
            page_length = 6+line_length
            continue
        
        page_contents.append(line)
        page_length += line_length
        continue
    
    limit = len(pages)
    index = 0
    while index < limit:
        embed = pages[index]
        index += 1
        embed.add_footer(f'page {index}/{limit}')
    
    await Pagination(client, message.channel, pages)

