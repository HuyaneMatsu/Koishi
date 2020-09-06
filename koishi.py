# -*- coding: utf-8 -*-
import re
from io import StringIO
from datetime import datetime, timedelta

from hata import BUILTIN_EMOJIS, Guild, Embed, Color, sleep, CLIENTS, USERS, CHANNELS, GUILDS, chunkify, Client, \
    Role, ChannelText, Invite, KOKORO
from hata.ext.commands import Pagination, checks, setup_ext_commands, Converter, ConverterFlag, Closer
from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand
from hata.ext.extension_loader import EXTENSION_LOADER

from tools import MessageDeleteWaitfor, GuildDeleteWaitfor, RoleDeleteWaitfor, ChannelDeleteWaitfor, \
    EmojiDeleteWaitfor, RoleEditWaitfor
from shared import KOISHI_PREFIX
from interpreter import Interpreter

DUNGEON = Guild.precreate(388267636661682178)

WELCOME_CHANNEL = ChannelText.precreate(445191707491958784)
EVERYNYAN_ROLE = Role.precreate(445189164703678464)
ANNOUNCEMNETS_ROLE = Role.precreate(538397994421190657)
WORSHIPPER_ROLE = Role.precreate(403586901803794432)
DUNGEON_PREMIUM_ROLE = Role.precreate(585556522558554113)
DUNGEON_INVITE = Invite.precreate('3cH2r5d')

KOISHI_HELP_COLOR = Color.from_html('#ffd21e')

_KOISHI_NOU_RP = re.compile(r'n+\s*o+\s*u+', re.I)
_KOISHI_OWO_RP = re.compile('(owo|uwu|0w0)', re.I)
_KOISHI_OMAE_RP = re.compile('omae wa mou', re.I)

KOISHI_DEFAULT_CATEGORY_NAME = 'Uncategorized'

def category_name_rule(name):
    if name is None:
        name = KOISHI_DEFAULT_CATEGORY_NAME
    else:
        name = name.capitalize()
    
    return name

setup_ext_commands(Koishi, KOISHI_PREFIX, default_category_name=KOISHI_DEFAULT_CATEGORY_NAME,
    category_name_rule=category_name_rule)

Koishi.events(MessageDeleteWaitfor)
Koishi.events(GuildDeleteWaitfor)
Koishi.events(RoleDeleteWaitfor)
Koishi.events(ChannelDeleteWaitfor)
Koishi.events(EmojiDeleteWaitfor)
Koishi.events(RoleEditWaitfor)

@Koishi.events
class once_on_ready(object):
    __slots__ = ('called',)
    __event_name__ = 'ready'
    
    def __init__(self):
        self.called = False
        
    async def __call__(self, client):
        if self.called:
            return
        
        self.called = True
        
        print(f'{client:f} ({client.id}) logged in\nowner: {client.owner:f} ({client.owner.id})')

Koishi.command_processer.create_category('TEST COMMANDS', checks=[checks.owner_only()])

Koishi.commands(SubterraneanHelpCommand(KOISHI_HELP_COLOR), 'help', category='HELP')

@Koishi.commands
async def default_event(client, message):
    user_mentions = message.user_mentions
    if (user_mentions is not None) and (client in user_mentions):
        m1 = message.author.mention
        m2 = client.mention
        m3 = message.author.mention_nick
        m4 = client.mention_nick
        replace = {
            '@everyone'   : '@\u200beveryone',
            '@here'       : '@\u200bhere',
            re.escape(m1) : m2,
            re.escape(m2) : m1,
            re.escape(m3) : m4,
            re.escape(m4) : m3,
                }
        pattern = re.compile("|".join(replace.keys()))
        result = pattern.sub(lambda x: replace[re.escape(x.group(0))], message.content)
        await client.message_create(message.channel, result)
        return
        
    content = message.content
    if message.channel.cached_permissions_for(client).can_add_reactions and (_KOISHI_NOU_RP.match(content) is not None):
        for value in 'nou':
            emoji = BUILTIN_EMOJIS[f'regional_indicator_{value}']
            await client.reaction_add(message,emoji)
        return
    
    matched = _KOISHI_OWO_RP.fullmatch(content,)
    if (matched is not None):
        text = f'{content[0].upper()}{content[1].lower()}{content[2].upper()}'
    
    elif (_KOISHI_OMAE_RP.match(content) is not None):
        text = 'NANI?'
    
    else:
        return
    
    await client.message_create(message.channel, text)

@Koishi.commands(checks=[checks.is_guild(DUNGEON)])
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
    while index<limit:
        embed = pages[index]
        index += 1
        embed.add_footer(f'page {index}/{limit}')
    
    await Pagination(client,message.channel,pages)
    return False

@Koishi.commands
async def invalid_command(client, message, command, content):
    prefix = client.command_processer.get_prefix_for(message)
    embed = Embed(
        f'Invalid command `{command}`',
        f'try using: `{prefix}help`',
        color=KOISHI_HELP_COLOR,
            )
    
    message = await client.message_create(message.channel,embed=embed)
    await sleep(30., KOKORO)
    await client.message_delete(message)

@Koishi.commands.from_class
class reload:
    async def command(client, message, name:str):
        while True:
            try:
                extension = EXTENSION_LOADER.extensions[name]
            except KeyError:
                result = 'There is no extension with the specified name'
                break
            
            if extension.locked:
                result = 'The extension is locked, propably for reason.'
                break
            
            try:
                await EXTENSION_LOADER.reload(name)
            except BaseException as err:
                result = repr(err)
                if len(result) > 2000:
                    result = result[-2000:]
                
                break
                
            result = 'success'
            break
        
        await client.message_create(message.channel, result)
        return
    
    category = 'UTILITY'
    checks = [checks.owner_only()]
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        lines = [
            'Reloads the specified extension by it\'s name.',
            f'Usage : `{prefix}reload <name>`',
            '\nAvailable extensions:',
                ]
        for extension in  EXTENSION_LOADER.extensions.values():
            lines.append(f'- `{extension.name}`{" (locked)" if extension.locked else ""}')
        
        pages = [Embed('reload', chunk, color=KOISHI_HELP_COLOR) for chunk in chunkify(lines)]
        
        limit = len(pages)
        index = 0
        while index<limit:
            embed = pages[index]
            index += 1
            embed.add_footer(f'page {index}/{limit}')
        
        return pages

async def execute_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('execute',(
        'Use an interpreter trough me :3\n'
        'Usages:\n'
        f'{prefix}execute #code here\n'
        '*not code*\n'
        '\n'
        f'{prefix}execute\n'
        '# code goes here\n'
        '# code goes here\n'
        '\n'
        f'{prefix}execute\n'
        '```\n'
        '# code goes here\n'
        '# code goes here\n'
        '```\n'
        '*not code*\n'
        '\n'
        '... and many more ways.'
            ), color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')

Koishi.commands(Interpreter(locals().copy()), name='execute',description=execute_description, category='UTILITY',
    checks=[checks.owner_only()])


PATTERN_ROLE_RELATION = [
    (re.compile('nya+', re.I), EVERYNYAN_ROLE, timedelta(minutes=10), True),
    (re.compile('[il] *meow+', re.I), ANNOUNCEMNETS_ROLE, timedelta(), True),
    (re.compile('[il] *not? *meow+', re.I), ANNOUNCEMNETS_ROLE, timedelta(), False),
    (re.compile('nekogirl', re.I), WORSHIPPER_ROLE, timedelta(days=183), True),
        ]

async def role_giver(client, message):
    for pattern, role, delta, add in PATTERN_ROLE_RELATION:
        
        if (pattern.fullmatch(message.content) is None):
            continue
        
        user = message.author
        if add == user.has_role(role):
            break
        
        guild_profile = user.guild_profiles.get(DUNGEON)
        if guild_profile is None:
            break
        
        joined_at = guild_profile.joined_at
        if joined_at is None:
            break
        
        if datetime.utcnow() - joined_at < delta:
            break
        
        permissions = message.channel.cached_permissions_for(client)
        if (not permissions.can_manage_roles) or (not client.has_higher_role_than(role)):
            if permissions.can_send_messages:
                content = 'My permissions are broken, cannot provide the specified role.'
            else:
                break
        else:
            await (Client.user_role_add if add else Client.user_role_delete)(client, user, role)
            
            if permissions.can_send_messages:
                if add:
                    content = f'You now have {role.mention} role.'
                else:
                    content = f'You have {role.mention} removed.'
            
            else:
                break
        
        message = await client.message_create(message.channel, content, allowed_mentions=None)
        await sleep(30.0)
        await client.message_delete(message)
        break

Koishi.command_processer.append(WELCOME_CHANNEL, role_giver)
