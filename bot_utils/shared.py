# -*- coding: utf-8 -*-
import os
from io import StringIO
from hata import ChannelText, Guild, Role, Invite, Color, Embed, KOKORO, ChannelCategory, Emoji, User
from hata.ext.commands import Pagination

import config

from config import KOISHI_PATH as PATH__KOISHI
if PATH__KOISHI is None:
    PATH__KOISHI = os.path.abspath('..')

PREFIX__KOISHI = config.KOISHI_PREFIX
PREFIX__SATORI = config.SATORI_PREFIX
PREFIX__FLAN = config.FLAN_PREFIX
PREFIX__MARISA = config.MARISA_PREFIX

GUILD__NEKO_DUNGEON = Guild.precreate(388267636661682178)

CHANNEL__NEKO_DUNGEON__SYSTEM = ChannelText.precreate(445191707491958784)
CHANNEL__NEKO_DUNGEON__EVENT = ChannelText.precreate(798911148292309002)
CHANNEL__NEKO_DUNGEON__DEFAULT_TEST = ChannelText.precreate(557187647831932938)

CHANNEL__SYSTEM__SYNC = ChannelText.precreate(568837922288173058)

ROLE__NEKO_DUNGEON__VERIFIED = Role.precreate(445189164703678464)
ROLE__NEKO_DUNGEON__ANNOUNCEMENTS = Role.precreate(538397994421190657)
ROLE__NEKO_DUNGEON__ELEVATED = Role.precreate(403586901803794432)
ROLE__NEKO_DUNGEON__BOOSTER = Role.precreate(585556522558554113)
ROLE__NEKO_DUNGEON__MODERATOR = Role.precreate(726171592509358093)
ROLE__NEKO_DUNGEON__TESTER = Role.precreate(648138238250319876)
ROLE__NEKO_DUNGEON__EVENT_MANAGER = Role.precreate(798913709019103284)

INVITE__NEKO_DUNGEON = Invite.precreate('3cH2r5d')

CATEGORY__NEKO_DUNGEON__BOTS = ChannelCategory.precreate(445191611727478795)

EMOJI__HEART_CURRENCY = Emoji.precreate(603533301516599296, name='youkai_kokoro')

COLOR__SATORI_HELP = Color.from_rgb(118, 0, 161)
COLOR__KOISHI_HELP = Color.from_html('#ffd21e')
COLOR__FLAN_HELP = Color.from_rgb(230, 69, 0)
COLOR__MARISA_HELP = Color.from_html('#e547ed')
COLOR__EVENT = Color(2316923)

LINK__KOISHI_GIT = 'https://github.com/HuyaneMatsu/Koishi'
LINK__HATA_GIT = 'https://github.com/HuyaneMatsu/hata'
LINK__HATA_DOCS = 'https://huyanematsu.pythonanywhere.com/docs/hata'
LINK__PASTE = 'https://hastebin.com/'
LINK__HATA_SLASH = 'https://github.com/HuyaneMatsu/hata/blob/master/docs/topics/slash.md'

USER__DISBOARD = User.precreate(302050872383242240, is_bot=True)

DEFAULT_CATEGORY_NAME = 'Uncategorized'

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

