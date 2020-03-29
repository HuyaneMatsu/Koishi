import re
from io import StringIO

from hata import BUILTIN_EMOJIS, Guild, Embed, Color, sleep, CLIENTS, USERS,\
    CHANNELS, GUILDS
from hata.events import Pagination, checks, setup_extension
from hata.dereaddons_local import function

from tools import MessageDeleteWaitfor, GuildDeleteWaitfor, RoleDeleteWaitfor,\
    ChannelDeleteWaitfor, EmojiDeleteWaitfor, RoleEditWaitfor
from shared import KOISHI_PREFIX
from interpreter import Interpreter

setup_extension(Koishi,KOISHI_PREFIX)

Koishi.events(MessageDeleteWaitfor)
Koishi.events(GuildDeleteWaitfor)
Koishi.events(RoleDeleteWaitfor)
Koishi.events(ChannelDeleteWaitfor)
Koishi.events(EmojiDeleteWaitfor)
Koishi.events(RoleEditWaitfor)

@Koishi.events
class once_on_ready(object):
    __slots__ = ('called',)
    __event_name__='ready'
    
    def __init__(self):
        self.called=False
        
    async def __call__(self,client):
        if self.called:
            return
        
        self.called=True
        
        print(f'{client:f} ({client.id}) logged in\nowner: {client.owner:f} ({client.owner.id})')

Koishi.command_processer.default_category_name='UNCATEGORIZED'
Koishi.command_processer.create_category('TEST COMMANDS',checks=[checks.owner_only()])

_KOISHI_NOU_RP=re.compile(r'n+\s*o+\s*u+',re.I)
_KOISHI_OWO_RP=re.compile('(owo|uwu|0w0)',re.I)
_KOISHI_OMAE_RP=re.compile('omae wa mou',re.I)

@Koishi.commands
async def default_event(client,message):
    user_mentions=message.user_mentions
    if (user_mentions is not None) and (client in user_mentions):
        m1=message.author.mention
        m2=client.mention
        m3=message.author.mention_nick
        m4=client.mention_nick
        replace={
            '@everyone':'@\u200beveryone',
            '@here':'@\u200bhere',
            re.escape(m1):m2,
            re.escape(m2):m1,
            re.escape(m3):m4,
            re.escape(m4):m3,
                }
        pattern=re.compile("|".join(replace.keys()))
        result=pattern.sub(lambda x: replace[re.escape(x.group(0))],message.content)
        await client.message_create(message.channel,result)
        return
        
    content=message.content
    if message.channel.cached_permissions_for(client).can_add_reactions and _KOISHI_NOU_RP.match(content) is not None:
        for value in 'nou':
            emoji=BUILTIN_EMOJIS[f'regional_indicator_{value}']
            await client.reaction_add(message,emoji)
        return
    
    matched=_KOISHI_OWO_RP.fullmatch(content,)
    if (matched is not None):
        text=f'{content[0].upper()}{content[1].lower()}{content[2].upper()}'
    
    elif _KOISHI_OMAE_RP.match(content) is not None:
        text='NANI?'
    
    else:
        return
    
    await client.message_create(message.channel,text)

DUNGEON=Guild.precreate(388267636661682178)

@Koishi.commands
async def command_error(client, message, command, content, exception):
    if message.guild is not DUNGEON:
        return True
    
    with StringIO() as buffer:
        await client.loop.render_exc_async(exception,[
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

KOISHI_HELP_COLOR=Color.from_html('#ffd21e')

async def help_description(client,message):
    by_categories=[]
    for category in client.command_processer.categories:
        if category.run_checks(client,message):
            command_names = []
            for command in category.commands:
                if command.run_checks(client,message):
                    command_names.append(command.name)
            
            # filter out empty categories
            if command_names:
                by_categories.append((f'**{category.name}**',command_names),)
    
    pages = []
    page = []
    page_line_count=0
    for category_name, command_names in by_categories:
        if page_line_count>14:
            pages.append('\n'.join(page))
            page.clear()
            page.append(category_name)
            page_line_count=1
        else:
            if page_line_count!=0:
                page.append('')
                page_line_count+=1
            page.append(category_name)
            page_line_count+=1
        
        for command_name in command_names:
            page.append(command_name)
            page_line_count+=1
            
            if page_line_count<20:
                continue
                
            pages.append('\n'.join(page))
            page.clear()
            page.append(category_name)
            page_line_count=1
            continue
    
    if page:
        pages.append('\n'.join(page))
    
    del page
    
    prefix=client.command_processer.prefix(message)
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

@Koishi.commands(description=help_description,category='HELP')
async def help(client, message, name:str=''):
    if not name:
        await help_description(client, message)
        return
    
    name = name.lower()
    command = client.command_processer.commands.get(name)
    
    if (command is None) or (not command.run_all_checks(client, message)):
        prefix=client.events.message_create.prefix(message)
        embed=Embed(f'Invalid command: {name!r}',(
            f'Please try using `{prefix}help` to list the available commands '
            'for you\n'
            'Take care!'
            ),color=KOISHI_HELP_COLOR)
        message = await client.message_create(message.channel,embed=embed)
        await sleep(30.,client.loop)
        await client.message_delete(message)
        return
    
    description=command.description
    if type(description) is function:
        await description(client, message)
        return
    
    if type(description) is str:
        await client.message_create(message.channel,embed=Embed(name,description,color=KOISHI_HELP_COLOR))
        return
    
    await client.message_create(message.channel,embed=Embed(description='The command has no description provided',color=KOISHI_HELP_COLOR))
    return

@Koishi.commands
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

@Koishi.commands.from_class
class about:
    async def command(client, message):
        implement=sys.implementation
        embed=Embed('About',(
            f'Me, {client.full_name}, I am general purpose/test client.'
            '\n'
            'My code base is'
            ' [open source](https://github.com/HuyaneMatsu/Koishi). '
            'One of the main goal of my existence is to test the best *cough*'
            ' [discord API wrapper](https://github.com/HuyaneMatsu/hata). '
            '\n\n'
            f'My Masutaa is {client.owner.full_name} (send neko pictures pls).\n\n'
            '**Client info**\n'
            f'Python version: {implement.version[0]}.{implement.version[1]}'
            f'{"" if implement.version[3]=="final" else " "+implement.version[3]}\n'
            f'Interpreter: {implement.name}\n'
            f'Clients: {len(CLIENTS)}\n'
            f'Users: {len(USERS)}\n'
            f'Guilds: {len(GUILDS)}\n'
            f'Channels: {len(CHANNELS)}\n'
            'Power level: over 9000!\n'
                )).add_thumbnail(client.application.icon_url_as(size=128))
        
        await client.message_create(message.channel,embed=embed)
    
    category = 'HELP'
    
    async def description(client, message):
        prefix=client.command_processer.prefix(message)
        embed=Embed('about',(
            'Just some information about me.'
            f'Usage: `{prefix}about`'
                ),color=KOISHI_HELP_COLOR)
        await client.message_create(message.channel,embed=embed)

async def execute_description(client,message):
    prefix=client.commandprocesser.prefix(message)
    embed=Embed('execute',(
        'Use an interpreter trough me :3\n'
        'Usages:\n'
        f'{prefix}execute #code here\n'
        '*not code*\n'
        '\n'
        f'{prefix}execute\n'
        '#code goes here\n'
        '#code goes here\n'
        '\n'
        f'{prefix}execute\n'
        '```\n'
        '#code goes here\n'
        '#code goes here\n'
        '```\n'
        '*not code*'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

Koishi.commands(Interpreter(locals().copy()),name='execute',description=execute_description,category='UTILITY',checks=[checks.owner_only()])
